<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Моя работа</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link active" to="/">Игра</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/platform">Платформа</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/genres">Жанр</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/director">Режиссер</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/studio">Студия</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/test">Тест</router-link>
            </li>
          </ul>
          <!-- Переключение между аккаунтами -->
          <div class="d-flex align-items-center me-3">
            <label class="me-2 mb-0" for="userSelect">Аккаунт:</label>
            <select id="userSelect" class="form-select form-select-sm" style="width:auto;" v-model="selectedUserId" @change="onUserChange">
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.name }}
              </option>
            </select>
          </div>
          <!-- Кнопка для входа в админку -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="btn btn-primary" href="/admin">Админка</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Предположим, что список пользователей вы можете получить с сервера.
// Для примера зададим статический список.
const users = ref([
  { id: 1, name: 'User 1' },
  { id: 2, name: 'User 2' },
  { id: 3, name: 'Admin (superuser)' },
]);

// По умолчанию выберем первого пользователя
const selectedUserId = ref(1);

// При переключении пользователя вы можете:
// - Записать этот user_id в глобальное хранилище,
// - Переподгрузить данные,
// - При запросах передавать user_id как query-параметр.
function onUserChange() {
  console.log('Текущий выбранный пользователь:', selectedUserId.value);
  // Здесь вы можете вызвать метод для обновления данных с учетом нового user_id.
  // Например, если это суперюзер, при запросах можно добавить ?user_id={selectedUserId.value}
}
</script>

<style scoped>
</style>
