<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";

const genres = ref([]);
const genreToAdd = ref({ name: '' });
const genreToEdit = ref({ id: null, name: '' });

async function fetchGenres() {
  try {
    const response = await axios.get("/api/genre/");
    genres.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении жанров:', error);
  }
}

onMounted(fetchGenres);

async function addGenre() {
  if (!genreToAdd.value.name) {
    alert("Введите название жанра");
    return;
  }
  try {
    await axios.post("/api/genre/", genreToAdd.value);
    await fetchGenres();
    genreToAdd.value.name = '';
  } catch (error) {
    console.error('Ошибка при добавлении жанра:', error);
  }
}

async function deleteGenre(id) {
  try {
    await axios.delete(`/api/genre/${id}/`);
    await fetchGenres();
  } catch (error) {
    console.error('Ошибка при удалении жанра:', error);
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>Жанры</h2>
    
    <!-- Форма добавления -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input type="text" class="form-control" v-model="genreToAdd.name" placeholder="Название жанра">
          <button class="btn btn-primary" @click="addGenre">Добавить</button>
        </div>
      </div>
    </div>

    <!-- Список жанров -->
    <div class="list-group">
      <div v-for="genre in genres" :key="genre.id" class="list-group-item d-flex justify-content-between align-items-center">
        {{ genre.name }}
        <button class="btn btn-danger btn-sm" @click="deleteGenre(genre.id)">Удалить</button>
      </div>
    </div>
  </div>
</template> 