<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios.js';
import { useTokenStore } from '@/stores/tokenStore';

const profile = ref(null);
const errorMessage = ref('');
const tokenStore = useTokenStore();


onMounted(async () => {
  try {
    const token = tokenStore.token;

    const response = await axios.get('/profile', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    profile.value = response.data;
  } catch (error) {
    console.error('Error fetching profile:', error);
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
      <p><strong>Interested In:</strong> {{ profile.interestedIn }}</p>
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
</style>
