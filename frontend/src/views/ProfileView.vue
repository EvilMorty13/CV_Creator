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
  <div class="profile-container">
    <h2>Profile Page</h2>

    <!-- Show the error message if it exists -->
    <p v-if="errorMessage">{{ errorMessage }}</p>

    <!-- Show the profile details if they are fetched successfully -->
    <div v-if="profile">
      <p><strong>User ID:</strong> {{ profile.user_id }}</p>
      <p><strong>Name:</strong> {{ profile.name }}</p>
      <p><strong>Interested In:</strong> {{ profile.interestedIn.join(', ') }}</p>
    </div>

    <!-- Show the skills if they are fetched successfully -->
    <div v-if="skills.length > 0">
      <h3>User Skills</h3>
      <div v-for="skill in skills" :key="skill.id" class="skill-item">
        <p><strong>Skill ID:</strong> {{ skill.id }}</p>
        <p><strong>Name:</strong> {{ skill.name }}</p>
        <p><strong>Level:</strong> {{ skill.level }}</p>
        <p><strong>Priority:</strong> {{ skill.priority }}</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.profile-container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.profile-container p {
  margin: 10px 0;
}

.skill-item {
  margin: 20px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
