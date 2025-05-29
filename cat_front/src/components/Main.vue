<script setup>
  import {ref} from 'vue'
  import { useRoute } from 'vue-router';

  const route = useRoute();
  const food = ref('')

  function get_query_str(feeding)
  {
    const login = route.query.login

    return feeding ? '@' + login + ' - ' + food.value + '~' : '@' + login + '~'
  }

 async function pet_the_cat() {
    const login = route.query.login

    const cat_query = get_query_str()

   console.log(cat_query)

    let res = await fetch('http://localhost:8080', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'cat_query': cat_query})
    }).then (
        res => res.json()
    )

    console.log(res.message)
    alert(res.message)
  }

  async function feed_the_cat(event) {
    const login = route.query.login

    const cat_query = '@' + login + ' - ' + food.value + '~'
    let res = await fetch('http://localhost:7070', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'cat_query': cat_query})
    }).then (
        res => res.json()
    )

    console.log(res.message)
    alert(res.message)
  }
</script>

<template>
  <div style = "position:absolute; left: 40%; top: 70%;">
    <input style = "height: 40px; width: 400px;" v-model = "food" placeholder = "Enter the food you want to feed your cat">
    <button style = "height: 44px;" @click = "feed_the_cat"> Feed the cat </button>
  </div>

  <div style = "position:absolute; left: 50%; top: 80%;">
    <button style = "height: 44px;" @click = "pet_the_cat"> Pet the cat </button>
  </div>
</template>

<style scoped>

</style>