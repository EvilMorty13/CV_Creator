<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios.js';
import { useTokenStore } from '@/stores/tokenStore';

const profile = ref(null);
const skills = ref([]); // Initialize skills as an empty array
const errorMessage = ref('');
const tokenStore = useTokenStore();

onMounted(async () => {
  try {
    const token = tokenStore.token;

    // Fetch profile details
    const profileResponse = await axios.get('/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    profile.value = profileResponse.data;

    // Fetch skills for the user
    const skillsResponse = await axios.get('/skill', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    skills.value = skillsResponse.data; // Populate the skills array
  } catch (error) {
    console.error('Error fetching data:', error);
    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.detail || 'An error occurred';
    } else {
      errorMessage.value = 'An error occurred';
    }
  }
});
</script>


<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-3xl font-bold text-center mb-6">Profile Page</h2>

    <!-- Show the error message if it exists -->
    <p v-if="errorMessage" class="text-red-500 text-center mb-4">{{ errorMessage }}</p>

    <!-- Show the profile details if they are fetched successfully -->
    <div v-if="profile" class="mb-6">
      <p class="text-lg"><strong>User ID:</strong> {{ profile.user_id }}</p>
      <p class="text-lg"><strong>Name:</strong> {{ profile.name }}</p>
      <p class="text-lg"><strong>Interested In:</strong> {{ profile.interestedIn.join(', ') }}</p>
    </div>

    <!-- Show the skills if they are fetched successfully -->
    <div v-if="skills.length > 0" class="mt-6">
      <h3 class="text-2xl font-semibold mb-4">User Skills</h3>
      <div v-for="skill in skills" :key="skill.id" class="bg-gray-100 p-4 mb-4 rounded-lg shadow-md grid grid-cols-4 gap-4">
        <p class="text-lg"><strong>Skill ID:</strong> {{ skill.id }}</p>
        <p class="text-lg"><strong>Name:</strong> {{ skill.name }}</p>
        <p class="text-lg"><strong>Level:</strong> {{ skill.level }}</p>
        <p class="text-lg"><strong>Priority:</strong> {{ skill.priority }}</p>
      </div>
    </div>
  </div>
</template>


