<template>
  <div class="flex flex-col justify-center items-center min-h-screen">
    <div class="text-center text-2xl font-bold mb-4">Home Page</div>
    <div class="flex flex-row gap-x-4">
      <RouterLink to="/profile">
        <button class="bg-blue-500 text-white px-4 py-2 rounded-lg mb-2 hover:bg-blue-700 transform transition duration-300 hover:scale-105">
          See Profile
        </button>
      </RouterLink>
      <RouterLink to="/update-profile">
        <button class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-700 transform transition duration-300 hover:scale-105">
          Update Profile
        </button>
      </RouterLink>
    </div>

  </div>
</template>
