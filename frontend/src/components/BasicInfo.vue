<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios.js';
import { useTokenStore } from '@/stores/tokenStore';

const tokenStore = useTokenStore();
const profile = ref(null);
const profileForm = ref({
  name: '',
  interestedIn: [],
});
const interestedInString = ref(null)
const editForm = ref(false);

const fetchProfile = async () => {
  try {
    const token = tokenStore.token;
    const response = await axios.get('/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    profile.value = response.data;
    profileForm.value = { ...response.data }; // Ensure the form has the current profile data
    interestedInString.value = profile.value.interestedIn.join(',');
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

const updateProfile = async () => {
  profileForm.value.interestedIn = interestedInString.value.split(',').map((item) => item.trim());
  try {
    const token = tokenStore.token;
    const response = await axios.put('/profile', profileForm.value, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    profile.value = response.data;
    editForm.value = false; // Exit edit mode
    alert('Profile updated successfully!');
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Failed to update profile. Try again.');
  }
};

onMounted(() => {
  fetchProfile();
});

</script>


<template>
   <h3 class="text-2xl font-semibold mb-4 text-center">Profile</h3>

<!-- Display profile details -->
<div v-if="!editForm && profile" class="mb-6">
  <p class="text-lg"><strong>User ID:</strong> {{ profile.user_id }}</p>
  <p class="text-lg"><strong>Name:</strong> {{ profile.name }}</p>
  <p class="text-lg"><strong>Interested In:</strong> {{ profile.interestedIn.join(',')}}</p>
  <button @click="editForm = true" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transform transition duration-300 mt-4"> Edit </button>
</div>


<!-- Inline edit form -->
<div v-if="editForm" class="mb-6">
    <label class="block mb-4">
      <span class="text-gray-700">Name:</span>
      <input
        v-model="profileForm.name"
        type="text"
        class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
      />
    </label>
    <label class="block mb-4">
      <span class="text-gray-700">Interested In:</span>
      <input
        v-model="interestedInString"
        type="text"
        class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-500"
      />
    </label>
    <div class="flex space-x-2">
      <button
        @click="updateProfile"
        class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-700 transform transition duration-300"
      >
        Save
      </button>
      <button
        @click="editForm = false"
        class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transform transition duration-300"
      >
        Cancel
      </button>
    </div>
  </div>
</template>
