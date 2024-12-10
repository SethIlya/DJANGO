<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";

const platforms = ref([]);
const platformToAdd = ref({ name: '' });
const platformToEdit = ref({ id: null, name: '' });

async function fetchPlatforms() {
  try {
    const response = await axios.get("/api/platform/");
    platforms.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении платформ:', error);
  }
}

onMounted(fetchPlatforms);

async function addPlatform() {
  if (!platformToAdd.value.name) {
    alert("Введите название платформы");
    return;
  }
  try {
    await axios.post("/api/platform/", platformToAdd.value);
    await fetchPlatforms();
    platformToAdd.value.name = '';
  } catch (error) {
    console.error('Ошибка при добавлении платформы:', error);
  }
}

async function deletePlatform(id) {
  try {
    await axios.delete(`/api/platform/${id}/`);
    await fetchPlatforms();
  } catch (error) {
    console.error('Ошибка при удалении платформы:', error);
  }
}

function editPlatform(platform) {
  platformToEdit.value = { ...platform };
}

async function updatePlatform() {
  if (!platformToEdit.value.name) {
    alert("Введите название платформы");
    return;
  }
  try {
    await axios.put(`/api/platform/${platformToEdit.value.id}/`, platformToEdit.value);
    await fetchPlatforms();
    platformToEdit.value = { id: null, name: '' };
  } catch (error) {
    console.error('Ошибка при обновлении платформы:', error);
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>Платформы</h2>
    
    <!-- Форма добавления -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input type="text" class="form-control" v-model="platformToAdd.name" placeholder="Название платформы">
          <button class="btn btn-primary" @click="addPlatform">Добавить</button>
        </div>
      </div>
    </div>

    <!-- Список платформ -->
    <div class="list-group">
      <div v-for="platform in platforms" :key="platform.id" class="list-group-item d-flex justify-content-between align-items-center">
        {{ platform.name }}
        <div>
          <button class="btn btn-sm btn-secondary me-2" @click="editPlatform(platform)" data-bs-toggle="modal" data-bs-target="#editPlatformModal">Редактировать</button>
          <button class="btn btn-danger btn-sm" @click="deletePlatform(platform.id)">Удалить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для редактирования платформы -->
    <div class="modal fade" id="editPlatformModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать платформу</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control" v-model="platformToEdit.name" placeholder="Название платформы">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="updatePlatform" data-bs-dismiss="modal">Сохранить</button>
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