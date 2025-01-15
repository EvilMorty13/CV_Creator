<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios.js';
import { useTokenStore } from '@/stores/tokenStore';

const skills = ref([]);
const errorMessage = ref('');
const tokenStore = useTokenStore();
const editingSkillId = ref(null);
const skillFormVisible = ref(false);
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
    editingSkillId.value = null;
    fetchSkills(); // Refresh the skill list
    alert('Skill updated successfully!');
  } catch (error) {
    console.error('Error updating skill:', error);
    alert('Failed to update skill. Try again.');
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
    skillFormVisible.value = false;
    resetForm();
    fetchSkills(); // Refresh the skill list
    alert('Skill added successfully!');
  } catch (error) {
    console.error('Error adding skill:', error);
    alert('Failed to add skill. Try again.');
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
    fetchSkills(); // Refresh the skill list
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

onMounted(() => {
  fetchSkills();
});

</script>


<template>
    <!-- Show error message -->
    <p v-if="errorMessage" class="text-red-500 text-center mb-4">{{ errorMessage }}</p>

    <!-- List all skills -->
    <div v-if="skills.length" class="mb-6">
      <h3 class="text-2xl font-semibold mb-4 text-center">Skills</h3>
        <div v-for="skill in skills" :key="skill.id">

          <!-- Inline editing -->
          <div v-if="editingSkillId !== skill.id" class="bg-gray-100 p-4 mb-4 rounded-lg shadow-md grid grid-cols-5 gap-4 items-center">
            <p class="text-lg"><strong>Name:</strong> {{ skill.name }}</p>
            <p class="text-lg"><strong>Level:</strong> {{ skill.level }}</p>
            <p class="text-lg"><strong>Priority:</strong> {{ skill.priority }}</p>
            <button
                @click="editingSkillId = skill.id"
                class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transform transition duration-300"
                >
                Edit
            </button>
            <button
                @click="deleteSkill(skill.id)"
                class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transform transition duration-300"
              >
                Delete
            </button>
          </div>
          <div v-else class="bg-gray-100 p-4 mb-4 rounded-lg shadow-md grid grid-cols-5 gap-4 items-center">
            <label class="block">
              <span class="text-gray-700">Name:</span>
              <input
                v-model="skill.name"
                type="text"
                class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
              />
            </label>
            <label class="block">
              <span class="text-gray-700">Level:</span>
              <input
                v-model.number="skill.level"
                type="number"
                min="1"
                max="10"
                class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
              />
            </label>
            <label class="block">
              <span class="text-gray-700">Priority:</span>
              <input
                v-model.number="skill.priority"
                type="number"
                min="1"
                class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
              />
            </label>
            <button
                @click="saveSkill(skill)"
                class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-700 transform transition duration-300"
              >
                Save
            </button>
            <button
                @click="editingSkillId = null"
                class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transform transition duration-300"
            >
                Cancel
            </button>
          </div>
        </div>
    </div>

    <!-- Add New Skill Button -->
    <div class="text-center mb-6">
      <button
        @click="skillFormVisible = !skillFormVisible"
        class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transform transition duration-300"
      >
        Add New Skill
      </button>
    </div>

    <!-- Add Skill Form -->
    <div
      v-if="skillFormVisible"
    >
      <h3 class="text-2xl font-semibold mb-4 text-center">Add Skill</h3>
      <form @submit.prevent="addSkill" class="bg-gray-100 p-4 mb-4 rounded-lg shadow-md grid grid-cols-5 gap-4 items-center">
        <label class="block">
          <span class="text-gray-700">Name:</span>
          <input
            v-model="skillForm.name"
            type="text"
            required
            class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
          />
        </label>
        <label class="block">
          <span class="text-gray-700">Level (1-10):</span>
          <input
            v-model.number="skillForm.level"
            type="number"
            min="1"
            max="10"
            required
            class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
          />
        </label>
        <label class="block">
          <span class="text-gray-700">Priority:</span>
          <input
            v-model.number="skillForm.priority"
            type="number"
            min="1"
            required
            class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
          />
        </label>
        <button
            type="submit"
            class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-700 transform transition duration-300"
          >
            Add
        </button>
        <button
            type="button"
            @click="resetForm"
            class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transform transition duration-300"
          >
            Cancel
        </button>
      </form>
    </div>
</template>

