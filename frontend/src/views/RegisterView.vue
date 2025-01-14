<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-semibold text-center mb-6">Register</h2>
      <form @submit.prevent="addUser">
        <div class="input-group mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            v-model="register.email"
            id="email"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
          />
        </div>
        <div class="input-group mb-4">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="register.password"
            id="password"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
          />
        </div>
        <div class="input-group mb-6">
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm Password</label>
          <input
            type="password"
            v-model="register.confirmPassword"
            id="confirmPassword"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
          />
        </div>
        <button
          type="submit"
          class="w-full py-2 text-white bg-blue-500 rounded hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-300"
        >
          Register
        </button>
      </form>
      <p class="mt-4 text-center text-sm">
        Already have an account?
        <router-link to="/" class="text-blue-500 hover:text-blue-700">Login</router-link>
      </p>
    </div>
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
    await axios.post('/register', {
      email: register.value.email,
      password: register.value.password,
    });

    // Redirect to login page after successful registration
    alert('Registration successful!');
    router.push('/');
  } catch (error) {
    console.error('Registration failed', error);
    alert('Registration failed, please try again.');
  }
};
</script>
