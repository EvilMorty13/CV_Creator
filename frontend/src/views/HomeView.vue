<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

function handleSeeProfile(){
  router.push('/profile');
}

</script>

<template>
  <div>Home Page</div>
  <button @click="handleSeeProfile">See profile</button>
</template>
