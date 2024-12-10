<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";

const studios = ref([]);
const studioToAdd = ref({ name: '' });
const studioToEdit = ref({ id: null, name: '' });

async function fetchStudios() {
  try {
    const response = await axios.get("/api/studio/");
    studios.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении студий:', error);
  }
}

onMounted(fetchStudios);

async function addStudio() {
  if (!studioToAdd.value.name) {
    alert("Введите название студии");
    return;
  }
  try {
    await axios.post("/api/studio/", studioToAdd.value);
    await fetchStudios();
    studioToAdd.value.name = '';
  } catch (error) {
    console.error('Ошибка при добавлении студии:', error);
  }
}

async function deleteStudio(id) {
  try {
    await axios.delete(`/api/studio/${id}/`);
    await fetchStudios();
  } catch (error) {
    console.error('Ошибка при удалении студии:', error);
  }
}

function editStudio(studio) {
  studioToEdit.value = { ...studio };
}

async function updateStudio() {
  if (!studioToEdit.value.name) {
    alert("Введите название студии");
    return;
  }
  try {
    await axios.put(`/api/studio/${studioToEdit.value.id}/`, studioToEdit.value);
    await fetchStudios();
    studioToEdit.value = { id: null, name: '' };
  } catch (error) {
    console.error('Ошибка при обновлении студии:', error);
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>Студии</h2>
    
    <!-- Форма добавления -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input type="text" class="form-control" v-model="studioToAdd.name" placeholder="Название студии">
          <button class="btn btn-primary" @click="addStudio">Добавить</button>
        </div>
      </div>
    </div>

    <!-- Список студий -->
    <div class="list-group">
      <div v-for="studio in studios" :key="studio.id" class="list-group-item d-flex justify-content-between align-items-center">
        {{ studio.name }}
        <div>
          <button class="btn btn-sm btn-secondary me-2" @click="editStudio(studio)" data-bs-toggle="modal" data-bs-target="#editStudioModal">Редактировать</button>
          <button class="btn btn-danger btn-sm" @click="deleteStudio(studio.id)">Удалить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для редактирования студии -->
    <div class="modal fade" id="editStudioModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать студию</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control" v-model="studioToEdit.name" placeholder="Название студии">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="updateStudio" data-bs-dismiss="modal">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>