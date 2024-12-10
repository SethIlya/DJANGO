<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";
import { Modal } from 'bootstrap';

const directors = ref([]);
const directorToAdd = ref({ name: '', surname: '', picture: null });
const directorToEdit = ref({ id: null, name: '', surname: '', picture: null });

const addPictureRef = ref(null);
const addImageUrl = ref('');
const editPictureRef = ref(null);
const editImageUrl = ref('');

const viewImageUrl = ref('');

async function fetchDirectors() {
  try {
    const response = await axios.get("/api/director/");
    // Убедитесь, что в response.data для каждого директора есть поле picture.
    console.log("Данные о руководителях:", response.data);
    directors.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении руководителей:', error);
  }
}

onMounted(fetchDirectors);

async function addDirector() {
  if (!directorToAdd.value.name || !directorToAdd.value.surname) {
    alert("Введите имя и фамилию руководителя");
    return;
  }

  try {
    const formData = new FormData();
    formData.append('name', directorToAdd.value.name);
    formData.append('surname', directorToAdd.value.surname);
    if (addPictureRef.value && addPictureRef.value.files.length > 0) {
      formData.append('picture', addPictureRef.value.files[0]);
    }

    console.log('Отправка данных при добавлении руководителя:', {
      name: directorToAdd.value.name,
      surname: directorToAdd.value.surname,
      hasPicture: addPictureRef.value && addPictureRef.value.files.length > 0
    });

    await axios.post("/api/director/", formData);
    await fetchDirectors();

    directorToAdd.value = { name: '', surname: '', picture: null };
    addImageUrl.value = '';
    if (addPictureRef.value) addPictureRef.value.value = '';
  } catch (error) {
    console.error('Ошибка при добавлении руководителя:', error);
  }
}

async function deleteDirector(id) {
  try {
    await axios.delete(`/api/director/${id}/`);
    await fetchDirectors();
  } catch (error) {
    console.error('Ошибка при удалении руководителя:', error);
  }
}

function editDirector(director) {
  directorToEdit.value = { ...director };
  editImageUrl.value = '';
  if (editPictureRef.value) editPictureRef.value.value = '';
}

async function updateDirector() {
  if (!directorToEdit.value.name || !directorToEdit.value.surname) {
    alert("Введите имя и фамилию руководителя");
    return;
  }

  try {
    const formData = new FormData();
    formData.append('name', directorToEdit.value.name);
    formData.append('surname', directorToEdit.value.surname);
    if (editPictureRef.value && editPictureRef.value.files.length > 0) {
      formData.append('picture', editPictureRef.value.files[0]);
    }

    console.log('Отправка данных при обновлении руководителя:', {
      id: directorToEdit.value.id,
      name: directorToEdit.value.name,
      surname: directorToEdit.value.surname,
      hasPicture: editPictureRef.value && editPictureRef.value.files.length > 0
    });

    await axios.put(`/api/director/${directorToEdit.value.id}/`, formData);
    await fetchDirectors();
    directorToEdit.value = { id: null, name: '', surname: '', picture: null };
    editImageUrl.value = '';
    if (editPictureRef.value) editPictureRef.value.value = '';
  } catch (error) {
    console.error('Ошибка при обновлении руководителя:', error);
  }
}

function addPictureChange() {
  if (addPictureRef.value && addPictureRef.value.files.length > 0) {
    addImageUrl.value = URL.createObjectURL(addPictureRef.value.files[0]);
  } else {
    addImageUrl.value = '';
  }
}

function editPictureChange() {
  if (editPictureRef.value && editPictureRef.value.files.length > 0) {
    editImageUrl.value = URL.createObjectURL(editPictureRef.value.files[0]);
  } else {
    editImageUrl.value = '';
  }
}

function openImageModal(imageUrl) {
  viewImageUrl.value = imageUrl;
  const modalEl = document.getElementById('viewImageModal');
  const modal = new Modal(modalEl);
  modal.show();
}

function closeImageModal() {
  const modalEl = document.getElementById('viewImageModal');
  const modal = Modal.getInstance(modalEl);
  if (modal) modal.hide();
}
</script>

<template>
  <div class="container mt-4">
    <h2>Руководители</h2>
    
    <!-- Форма добавления -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group mb-2">
          <input type="text" class="form-control" v-model="directorToAdd.name" placeholder="Имя руководителя">
          <input type="text" class="form-control" v-model="directorToAdd.surname" placeholder="Фамилия руководителя">
        </div>
        <div class="input-group mb-2">
          <input type="file" class="form-control" ref="addPictureRef" @change="addPictureChange">
        </div>
        <div v-if="addImageUrl" class="mb-2">
          <img :src="addImageUrl" style="max-height:60px;" alt="Предпросмотр">
        </div>
        <button class="btn btn-primary" @click="addDirector">Добавить</button>
      </div>
    </div>

    <!-- Список руководителей -->
    <div class="list-group">
      <div
        v-for="director in directors"
        :key="director.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <div>
          {{ director.name }} {{ director.surname }}
          <!-- Если есть картинка, показываем её и иконку лупы -->
          <div v-if="director.picture" class="image-container d-inline-block ms-3 position-relative">
            <img :src="director.picture" style="max-height:60px;" alt="Фото руководителя">
            <div class="zoom-icon" @click.stop="openImageModal(director.picture)">
              <i class="bi bi-zoom-in" style="color: white; font-size:24px;"></i>
            </div>
          </div>
          <!-- Если картинки нет, можно отобразить заглушку или ничего не показывать -->
          <!--
          <div v-else class="d-inline-block ms-3">
            <img src="/static/images/no-image.png" style="max-height:60px;" alt="Нет изображения">
          </div>
          -->
        </div>
        <div>
          <button class="btn btn-sm btn-secondary me-2" @click="editDirector(director)" data-bs-toggle="modal" data-bs-target="#editDirectorModal">Редактировать</button>
          <button class="btn btn-danger btn-sm" @click="deleteDirector(director.id)">Удалить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для редактирования руководителя -->
    <div class="modal fade" id="editDirectorModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать руководителя</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control mb-2" v-model="directorToEdit.name" placeholder="Имя руководителя">
            <input type="text" class="form-control mb-2" v-model="directorToEdit.surname" placeholder="Фамилия руководителя">
            <input type="file" class="form-control mb-2" ref="editPictureRef" @change="editPictureChange">
            <div v-if="editImageUrl" class="mb-2">
              <img :src="editImageUrl" style="max-height:100px; cursor:pointer;" @click="openImageModal(editImageUrl)" alt="Предпросмотр">
            </div>
            <div v-else-if="directorToEdit.picture" class="mb-2">
              <img :src="directorToEdit.picture" style="max-height:100px; cursor:pointer;" @click="openImageModal(directorToEdit.picture)" alt="Текущее изображение">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="updateDirector" data-bs-dismiss="modal">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для просмотра изображения -->
    <div class="modal fade" id="viewImageModal" tabindex="-1" aria-labelledby="viewImageModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewImageModalLabel">Просмотр изображения</h5>
            <button type="button" class="btn-close" @click="closeImageModal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="viewImageUrl" class="img-fluid" alt="Просматриваемое изображение">
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

.image-container {
  position: relative;
  display: inline-block;
}

.zoom-icon {
  position: absolute; 
  top: 50%; 
  left: 50%; 
  transform: translate(-50%, -50%); 
  cursor: pointer; 
  background: rgba(0,0,0,0.5); 
  border-radius: 50%; 
  padding: 10px;
  display: none;
}

.image-container:hover .zoom-icon {
  display: block;
}
</style>
