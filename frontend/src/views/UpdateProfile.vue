<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios.js';
import { useTokenStore } from '@/stores/tokenStore';

const skills = ref([]);
const errorMessage = ref('');
const tokenStore = useTokenStore();
const editingSkillId = ref(null); // Tracks which skill is being edited
const skillFormVisible = ref(false); // Tracks visibility of the "Add Skill" form
const skillForm = ref({
  id: null,
  name: '',
  level: '',
  priority: '',
});

const fetchSkills = async () => {
  try {
    const token = tokenStore.token;
    const response = await axios.get('/skill', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    skills.value = response.data;
  } catch (error) {
    console.error('Error fetching skills:', error);
    errorMessage.value = error.response?.data?.detail || 'An error occurred';
  }
};

const saveSkill = async (skill) => {
  try {
    const token = tokenStore.token;
    await axios.put(`/skill/${skill.id}`, skill, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    alert('Skill updated successfully!');
    editingSkillId.value = null; // Exit edit mode
  } catch (error) {
    console.error('Error updating skill:', error);
    alert('Failed to update skill. Check the input and try again.');
  }
};

const addSkill = async () => {
  try {
    const token = tokenStore.token;
    await axios.post('/skill', skillForm.value, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    fetchSkills()
    alert('Skill added successfully!');
    resetForm(); // Reset the form
  } catch (error) {
    console.error('Error adding skill:', error);
    alert('Failed to add skill. Check the input and try again.');
  }
};

const deleteSkill = async (skillId) => {
  try {
    const token = tokenStore.token;
    await axios.delete(`/skill/${skillId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    fetchSkills()
    alert('Skill deleted successfully!');
  } catch (error) {
    console.error('Error deleting skill:', error);
    alert('Failed to delete skill. Try again.');
  }
};

const resetForm = () => {
  skillForm.value = { id: null, name: '', level: '', priority: '' };
  skillFormVisible.value = false;
};

onMounted(fetchSkills);
</script>

<template>
  <div class="update-profile-container">
    <h2>Update Profile</h2>

    <!-- Show error message -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- List all skills -->
    <div v-if="skills.length">
      <h3>Skills</h3>
      <ul>
        <li v-for="skill in skills" :key="skill.id">
          <!-- Inline editing -->
          <div v-if="editingSkillId !== skill.id">
            <p>
              <strong>Name:</strong>
              {{ skill.name }}
            </p>
            <p>
              <strong>Level:</strong>
              {{ skill.level }}
            </p>
            <p>
              <strong>Priority:</strong>
              {{ skill.priority }}
            </p>
            <button @click="editingSkillId = skill.id">Edit</button>
            <button @click="deleteSkill(skill.id)">Delete</button>
          </div>
          <div v-else>
            <label>
              Name:
              <input v-model="skill.name" type="text" />
            </label>
            <label>
              Level:
              <input v-model.number="skill.level" type="number" min="1" max="10" />
            </label>
            <label>
              Priority:
              <input v-model.number="skill.priority" type="number" min="1" />
            </label>
            <button @click="saveSkill(skill)">Save</button>
            <button @click="editingSkillId = null">Cancel</button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Add New Skill Button -->
    <button @click="skillFormVisible = !skillFormVisible">Add New Skill</button>

    <!-- Add Skill Form -->
    <div v-if="skillFormVisible" class="skill-form">
      <h3>Add Skill</h3>
      <form @submit.prevent="addSkill">
        <label>
          Name:
          <input v-model="skillForm.name" type="text" required />
        </label>
        <label>
          Level (1-10):
          <input v-model.number="skillForm.level" type="number" min="1" max="10" required />
        </label>
        <label>
          Priority:
          <input v-model.number="skillForm.priority" type="number" min="1" required />
        </label>
        <button type="submit">Add</button>
        <button type="button" @click="resetForm">Cancel</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.update-profile-container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.error-message {
  color: red;
  margin-bottom: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}

button {
  margin: 5px;
  padding: 10px 15px;
  cursor: pointer;
}

label {
  display: block;
  margin-bottom: 10px;
}
</style>
