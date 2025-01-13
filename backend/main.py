from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from database import *
from models import *
from auth import *
from schemas import *


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=CreateUserResponse)
async def register(request: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    hashed_password = bcrypt_context.hash(request.password)
    new_user = Users(email=request.email, password=hashed_password, isAdmin=False)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return CreateUserResponse(email=new_user.email, password=new_user.password, isAdmin=new_user.isAdmin)


@app.post("/login", response_model=Token) # OAuth2PasswordRequestForm is used for swagger authentication
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(Users).where(Users.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not bcrypt_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"id": user.id, "email": user.email, "isAdmin": user.isAdmin}
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_bearer)]):
    print(token)
    await blacklist_the_token(token)
    return {"message": "Successfully logged out"}

@app.post("/profile", response_model=CreateProfileResponse)
async def create_profile(
    profile_data: CreateProfileRequest,
    token: Annotated[str, Depends(oauth2_bearer)],
    db: AsyncSession = Depends(get_db)):

    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )

    # Get the current user using the provided token
    current_user = await get_current_user(token, db)
    
    # Check if the profile already exists for the current user
    existing_profile = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    existing_profile = existing_profile.scalars().first()

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user."
        )

    # Create the profile if it doesn't exist
    new_profile = Profile(
        user_id=current_user.id,
        name=profile_data.name,
        interestedIn=profile_data.interestedIn
    )
    
    # Add profile to database
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    
    # Return response with profile data
    return CreateProfileResponse(
        user_id=new_profile.user_id,
        name=new_profile.name,
        interestedIn=new_profile.interestedIn
    )




@app.get("/profile", response_model=CreateProfileResponse)
async def get_profile(
    token: Annotated[str, Depends(oauth2_bearer)],  
    db: AsyncSession = Depends(get_db)):

    # Check if the token is blacklisted
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )
    
    # Get the current user using the provided token
    current_user = await get_current_user(token, db)
    
    profile_query = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = profile_query.scalars().first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    

    return CreateProfileResponse(
        user_id=profile.user_id,
        name=profile.name,
        interestedIn=profile.interestedIn
    )

@app.put("/profile", response_model=CreateProfileResponse)
async def update_profile(
    profile_data: CreateProfileRequest,
    token: Annotated[str, Depends(oauth2_bearer)],  
    db: AsyncSession = Depends(get_db)):


    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )
    
    current_user = await get_current_user(token, db)
    
    profile_query = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = profile_query.scalars().first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    

    profile.name = profile_data.name
    profile.interestedIn = profile_data.interestedIn
    

    await db.commit()
    await db.refresh(profile)
    
    return CreateProfileResponse(
        user_id=profile.user_id,
        name=profile.name,
        interestedIn=profile.interestedIn
    )

@app.delete("/profile", response_model=dict)
async def delete_profile(
    token: Annotated[str, Depends(oauth2_bearer)], 
    db: AsyncSession = Depends(get_db)  ):


    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )
    
    current_user = await get_current_user(token, db)
    
    profile_query = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = profile_query.scalars().first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    await db.delete(profile)
    await db.commit()


    return {"detail": "Profile deleted successfully"}


@app.post("/skill", response_model=CreateSkillResponse)
async def create_skill(
    skill_data: CreateSkillRequest,
    token: Annotated[str, Depends(oauth2_bearer)],
    db: AsyncSession = Depends(get_db)
):
    # Check if the token is blacklisted
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )
    
    # Get the current user using the provided token
    current_user = await get_current_user(token, db)

    # Validate that the user exists
    user_query = await db.execute(select(Users).where(Users.id == current_user.id))
    user = user_query.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Create a new skill for the user
    new_skill = Skill(
        user_id=current_user.id,
        name=skill_data.name,
        level=skill_data.level,
        priority=skill_data.priority
    )

    # Add the new skill to the database
    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)

    # Return the created skill as a response
    return CreateSkillResponse(
        id=new_skill.id,
        user_id=new_skill.user_id,
        name=new_skill.name,
        level=new_skill.level,
        priority=new_skill.priority
    )

@app.get("/skill", response_model=List[CreateSkillResponse])
async def get_skills(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: AsyncSession = Depends(get_db)
):
    # Check if the token is blacklisted
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )
    
    # Get the current user using the provided token
    current_user = await get_current_user(token, db)

    # Query all skills for the current user
    skills_query = await db.execute(
        select(Skill).where(Skill.user_id == current_user.id)
    )
    skills = skills_query.scalars().all()

    if not skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No skills found for the current user."
        )

    # Return the skills as a response
    return [
        CreateSkillResponse(
            id=skill.id,
            user_id=skill.user_id,
            name=skill.name,
            level=skill.level,
            priority=skill.priority
        )
        for skill in skills
    ]


@app.put("/skill/{skill_id}", response_model=CreateSkillResponse)
async def update_skill(
    skill_id: int,
    skill_data: CreateSkillRequest,
    token: Annotated[str, Depends(oauth2_bearer)],
    db: AsyncSession = Depends(get_db)
):
    # Check if the token is blacklisted
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )

    # Get the current user using the provided token
    current_user = await get_current_user(token, db)

    # Fetch the skill to be updated
    skill_query = await db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    )
    skill = skill_query.scalars().first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found."
        )

    # Update the skill fields
    skill.name = skill_data.name
    skill.level = skill_data.level
    skill.priority = skill_data.priority

    # Commit the changes to the database
    await db.commit()
    await db.refresh(skill)

    # Return the updated skill
    return CreateSkillResponse(
        id=skill.id,
        user_id=skill.user_id,
        name=skill.name,
        level=skill.level,
        priority=skill.priority
    )


@app.delete("/skill/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: int,
    token: Annotated[str, Depends(oauth2_bearer)],
    db: AsyncSession = Depends(get_db)
):
    # Check if the token is blacklisted
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again."
        )

    # Get the current user using the provided token
    current_user = await get_current_user(token, db)

    # Fetch the skill to be deleted
    skill_query = await db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    )
    skill = skill_query.scalars().first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found."
        )

    # Delete the skill from the database
    await db.delete(skill)
    await db.commit()

    # Return a 204 No Content response
    return None


# @app.get("/test")
# async def test(
#     token: Annotated[str, Depends(oauth2_bearer)],
#     current_user: Users = Depends(get_current_user)):

#     if token in token_blacklist:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has been revoked. Please log in again."
#         )
    
#     return {"message": "This is a test", "email": current_user.email}

