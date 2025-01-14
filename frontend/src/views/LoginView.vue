<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm p-6 bg-white rounded-lg shadow-md  border-black	">
      <h2 class="text-2xl font-semibold text-center text-gray-700 mb-6">Login</h2>
      <form @submit.prevent="loginUser" class="space-y-4">
        <div class="flex flex-col">
          <label for="email" class="mb-1 text-sm font-medium text-gray-600">Email</label>
          <input
            type="email"
            v-model="login.email"
            id="email"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
          />
        </div>
        <div class="flex flex-col">
          <label for="password" class="mb-1 text-sm font-medium text-gray-600">Password</label>
          <input
            type="password"
            v-model="login.password"
            id="password"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
          />
        </div>
        <button
          type="submit"
          class="w-full py-2 text-white bg-blue-500 rounded hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-300"
        >
          Login
        </button>
      </form>
      <p class="mt-4 text-sm text-center text-gray-600">
        Don't have an account?
        <router-link to="/register" class="text-blue-500 hover:underline">Register</router-link>
      </p>
    </div>
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
/* No additional styles needed since Tailwind CSS is used */
</style>
