<template>
  <div style="max-width: 600px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; font-family: sans-serif;">
    <h2>Личный кабинет</h2>
    <div v-if="user">
      <p><strong>Имя:</strong> {{ user.name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <hr>
      <p><em>Здесь будет редактирование профиля, выбор профессии и тесты.</em></p>
    </div>
    <div v-else>
      <p>Загрузка данных...</p>
    </div>
    <button @click="logout" style="margin-top: 20px; background: #ff4d4d; color: white; padding: 8px; border: none; cursor: pointer;">Выйти</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const user = ref(null)
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  try {
    const response = await axios.get('http://localhost:8000/api/users/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    user.value = response.data
  } catch (err) {
    localStorage.removeItem('token')
    router.push('/login')
  }
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>