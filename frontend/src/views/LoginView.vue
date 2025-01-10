<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div class="input-group">
        <label for="email">Email</label>
        <input type="email" v-model="login.email" id="email" required />
      </div>
      <div class="input-group">
        <label for="password">Password</label>
        <input type="password" v-model="login.password" id="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useTokenStore } from '@/stores/tokenStore';
import axios from '@/axios.js';

const login = ref({
  email: '',
  password: '',
});

const router = useRouter();
const tokenStore = useTokenStore();
const loginUser = async () => {
  try {
    const response = await axios.post('/login', new URLSearchParams({
      username: login.value.email,
      password: login.value.password,
    }).toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    // Save the token using Pinia store
    tokenStore.setToken(response.data.access_token);

    // Redirect to the home page after successful login
    router.push('/home');
  } catch (error) {
    console.error('Login failed', error.response ? error.response.data : error);
    alert('Invalid credentials');
  }
};
</script>


<style scoped>
.login-container {
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
