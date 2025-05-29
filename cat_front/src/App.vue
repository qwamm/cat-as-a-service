<script setup>
import {ref} from 'vue'
import {useRouter } from 'vue-router'
const login = ref('')
const router = useRouter()

function handle_login_input(event) {
  console.log(login.value)
  if (login.value !== '')
  {
    router.push({path: '/main', query: {login: login.value}})
  }
}

</script>

<template>
  <header>
    <h1>
      MEPhI Networks 2025 External
    </h1>
  </header>
  <div style = "position:absolute; left: 38%; top: 9%;">
    <img src="./assets/cat.png">
  </div>

  <div style = "position:absolute; left: 30%; top: 60%;">
    <input style = "height: 40px; width: 800px;" v-model = "login" placeholder = "Enter your username to access the cat service">
    <button style = "height: 44px;" @click = "handle_login_input"> Log in </button>
  </div>

  <router-view></router-view>
</template>

<style scoped>
header {
  position: absolute;
  top: 1%;
  left: 38%;
  font-weight: bold;
  font-size: 1.2rem;
}
</style>