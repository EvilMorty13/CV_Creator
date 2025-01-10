<!-- src/views/RegisterView.vue -->
<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="addUser">
      <div class="input-group">
        <label for="email">Email</label>
        <input type="email" v-model="register.email" id="email" required />
      </div>
      <div class="input-group">
        <label for="password">Password</label>
        <input type="password" v-model="register.password" id="password" required />
      </div>
      <div class="input-group">
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" v-model="register.confirmPassword" id="confirmPassword" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <router-link to="/">Login</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from '@/axios.js';

const register = ref({
  email: '',
  password: '',
  confirmPassword: '',
});

const router = useRouter();

const addUser = async () => {
  if (register.value.password !== register.value.confirmPassword) {
    alert('Passwords do not match!');
    return;
  }

  try {
    const response = await axios.post('/register', {
      email: register.value.email,
      password: register.value.password,
    });

    // Redirect to login page after successful registration
    alert('Registration successful!');
    router.push('/');
  } catch (error) {
    console.error('Registration failed', error.response ? error.response.data : error);
    alert('Registration failed, please try again.');
  }
};
</script>

<style scoped>
.register-container {
  width: 300px;
  margin: auto;
  padding: 20px;
}
.input-group {
  margin-bottom: 15px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
}
</style>
