<script setup>
import { computed, ref, onBeforeMount, onMounted } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import _ from 'lodash';
import { Modal } from 'bootstrap';

const gamesToAdd = ref({ name: '', genre: null, studio: null, director: null, platform: null, picture: null });
const gamesToEdit = ref({ name: '', genre: null, studio: null, director: null, platform: null, picture: null });

const games = ref([]);
const genres = ref([]);
const studios = ref([]);
const directors = ref([]);
const platforms = ref([]);

const gamesPictureRef = ref(null);
const gamesAddImageUrl = ref('');
const editPictureRef = ref(null);
const editImageUrl = ref('');
const viewImageUrl = ref(''); // URL изображения для просмотра

// Поле для фильтра по имени пользователя
const filterUsername = ref('');

// Устанавливаем CSRF токен при монтировании
onMounted(() => {
  const csrfToken = Cookies.get('csrftoken');
  if (csrfToken) {
    axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  } else {
    console.warn('CSRF токен не найден.');
  }
});

// Загрузка данных с учетом фильтра по username, если указан
async function fetchGames() {
  try {
    let url = "/api/games/";
    if (filterUsername.value) {
      url += `?username=${encodeURIComponent(filterUsername.value)}`;
    }
    const response = await axios.get(url);
    games.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении игр:', error);
  }
}

async function fetchGenres() {
  try {
    const response = await axios.get("/api/genre/");
    genres.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении жанров:', error);
  }
}

async function fetchStudios() {
  try {
    const response = await axios.get("/api/studio/");
    studios.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении студий:', error);
  }
}

async function fetchDirectors() {
  try {
    const response = await axios.get("/api/director/");
    directors.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении руководителей:', error);
  }
}

async function fetchPlatforms() {
  try {
    const response = await axios.get("/api/platform/");
    platforms.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении платформ:', error);
  }
}

onBeforeMount(async () => {
  await fetchGenres();
  await fetchStudios();
  await fetchDirectors();
  await fetchPlatforms();
  await fetchGames();
});

const genreById = computed(() => _.keyBy(genres.value, 'id'));
const studioById = computed(() => _.keyBy(studios.value, 'id'));
const directorById = computed(() => _.keyBy(directors.value, 'id'));
const platformById = computed(() => _.keyBy(platforms.value, 'id'));

async function onGamesAdd() {
  if (!gamesToAdd.value.name) {
    alert("Пожалуйста, заполните 'Название игры'.");
    return;
  }
  if (!gamesToAdd.value.genre || !gamesToAdd.value.studio || !gamesToAdd.value.director || !gamesToAdd.value.platform) {
    alert("Пожалуйста, заполните все поля.");
    return;
  }

  try {
    const formData = new FormData();
    if (gamesPictureRef.value && gamesPictureRef.value.files.length > 0) {
      formData.append('picture', gamesPictureRef.value.files[0]);
    }

    formData.set('name', gamesToAdd.value.name);
    formData.set('platform', gamesToAdd.value.platform);
    formData.set('genre', gamesToAdd.value.genre);
    formData.set('studio', gamesToAdd.value.studio);
    formData.set('director', gamesToAdd.value.director);

    await axios.post("/api/games/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    await fetchGames();
    gamesToAdd.value = { name: '', genre: null, studio: null, director: null, platform: null, picture: null };
    gamesAddImageUrl.value = '';
    if (gamesPictureRef.value) {
      gamesPictureRef.value.value = '';
    }

  } catch (error) {
    console.error('Ошибка при добавлении игры:', error);
  }
}

async function onGamesDelete(game) {
  try {
    await axios.delete(`/api/games/${game.id}`);
    await fetchGames();
  } catch (error) {
    console.error('Ошибка при удалении игры:', error);
  }
}

function onGamesEdit(game) {
  gamesToEdit.value = { ...game };
  editImageUrl.value = '';
  if (editPictureRef.value) {
    editPictureRef.value.value = '';
  }
}

async function onUpdateGames() {
  if (!gamesToEdit.value.name || !gamesToEdit.value.genre || !gamesToEdit.value.studio || !gamesToEdit.value.director || !gamesToEdit.value.platform) {
    alert("Пожалуйста, заполните все поля для редактирования.");
    return;
  }

  try {
    const formData = new FormData();
    formData.set('name', gamesToEdit.value.name);
    formData.set('platform', gamesToEdit.value.platform);
    formData.set('genre', gamesToEdit.value.genre);
    formData.set('studio', gamesToEdit.value.studio);
    formData.set('director', gamesToEdit.value.director);

    if (editPictureRef.value && editPictureRef.value.files.length > 0) {
      formData.append('picture', editPictureRef.value.files[0]);
    }

    await axios.put(`/api/games/${gamesToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    await fetchGames();
    gamesToEdit.value = { name: '', genre: null, studio: null, director: null, platform: null, picture: null };
    editImageUrl.value = '';
    if (editPictureRef.value) {
      editPictureRef.value.value = '';
    }

  } catch (error) {
    console.error('Ошибка при обновлении игры:', error);
  }
}

function gamesAddPictureChange() {
  if (gamesPictureRef.value && gamesPictureRef.value.files.length > 0) {
    gamesAddImageUrl.value = URL.createObjectURL(gamesPictureRef.value.files[0]);
  } else {
    gamesAddImageUrl.value = '';
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

// Применить фильтр по username
function applyUserFilter() {
  fetchGames();
}
</script>

<template>
  <!-- Модальное окно для редактирования игры -->
  <div class="modal fade" id="editGamesModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="gamesToEdit.name"
                  placeholder="Название игры"
                />
                <label>Название игры</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <select class="form-select" v-model="gamesToEdit.genre">
                  <option disabled value="">Выберите жанр</option>
                  <option :value="g.id" v-for="g in genres" :key="g.id">{{ g.name }}</option>
                </select>
                <label>Жанр</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <select class="form-select" v-model="gamesToEdit.studio">
                  <option disabled value="">Выберите студию</option>
                  <option :value="s.id" v-for="s in studios" :key="s.id">{{ s.name }}</option>
                </select>
                <label>Студия</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <select class="form-select" v-model="gamesToEdit.director">
                  <option disabled value="">Выберите руководителя</option>
                  <option :value="d.id" v-for="d in directors" :key="d.id">{{ d.name }} {{ d.surname }}</option>
                </select>
                <label>Руководитель</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <select class="form-select" v-model="gamesToEdit.platform">
                  <option disabled value="">Выберите платформу</option>
                  <option :value="p.id" v-for="p in platforms" :key="p.id">{{ p.name }}</option>
                </select>
                <label>Платформа</label>
              </div>
            </div>
            <div class="col-12">
              <label for="gamePictureEdit" class="form-label">Изображение</label>
              <input 
                class="form-control" 
                type="file" 
                ref="editPictureRef" 
                @change="editPictureChange" 
              >
              <div v-if="editImageUrl" class="mt-2">
                <img :src="editImageUrl" style="max-height: 100px; cursor: pointer;" @click="openImageModal(editImageUrl)" alt="Предпросмотр">
              </div>
              <div v-else-if="gamesToEdit.picture" class="mt-2">
                <img :src="gamesToEdit.picture" style="max-height: 100px; cursor: pointer;" @click="openImageModal(gamesToEdit.picture)" alt="Текущее изображение">
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateGames"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Форма добавления новой игры -->
  <div class="p-2">
    <div class="row mb-4 align-items-end">
      <div class="col">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            v-model="gamesToAdd.name"
            placeholder="Название игры"
          />
          <label>Название игры</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <select class="form-select" v-model="gamesToAdd.genre">
            <option disabled value="">Выберите жанр</option>
            <option :value="g.id" v-for="g in genres" :key="g.id">{{ g.name }}</option>
          </select>
          <label>Жанр</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <select class="form-select" v-model="gamesToAdd.studio">
            <option disabled value="">Выберите студию</option>
            <option :value="s.id" v-for="s in studios" :key="s.id">{{ s.name }}</option>
          </select>
          <label>Студия</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <select class="form-select" v-model="gamesToAdd.director">
            <option disabled value="">Выберите руководителя</option>
            <option :value="d.id" v-for="d in directors" :key="d.id">{{ d.name }} {{ d.surname }}</option>
          </select>
          <label>Руководитель</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <select class="form-select" v-model="gamesToAdd.platform">
            <option disabled value="">Выберите платформу</option>
            <option :value="p.id" v-for="p in platforms" :key="p.id">{{ p.name }}</option>
          </select>
          <label>Платформа</label>
        </div>
      </div>
      <div class="col-auto">
        <label class="form-label">Изображение</label>
        <input 
          class="form-control" 
          type="file" 
          ref="gamesPictureRef" 
          @change="gamesAddPictureChange"
        >
        <div v-if="gamesAddImageUrl" class="mt-2">
          <img :src="gamesAddImageUrl" style="max-height: 60px;" alt="Предпросмотр">
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="onGamesAdd">Добавить</button>
      </div>
    </div>

    <!-- Поле ввода для фильтра по username и кнопка применить фильтр -->
    <div class="row mb-3">
      <div class="col-auto">
        <input type="text" class="form-control" v-model="filterUsername" placeholder="Имя пользователя для фильтрации">
      </div>
      <div class="col-auto">
        <button class="btn btn-info" @click="applyUserFilter">Применить фильтр</button>
      </div>
    </div>

    <!-- Список игр -->
    <div>
      <div v-for="item in games" :key="item.id" class="games-item mb-3 p-3 border rounded">
        <b>Название:</b> {{ item.name }} <br />
        <b>Жанр:</b> {{ genreById[item.genre]?.name }} <br />
        <b>Студия:</b> {{ studioById[item.studio]?.name }} <br />
        <b>Руководитель:</b> {{ directorById[item.director]?.name }} {{ directorById[item.director]?.surname }} <br />
        <b>Платформа:</b> {{ platformById[item.platform]?.name }} <br />
        <div v-if="item.picture" class="image-container mt-2" style="display:inline-block; position:relative;">
          <img 
            :src="item.picture" 
            class="preview-image" 
            style="max-height:60px;"
            alt="Изображение игры"
          >
          <div class="zoom-icon" @click.stop="openImageModal(item.picture)">
            <i class="bi bi-zoom-in" style="color: white; font-size:24px;"></i>
          </div>
        </div>
        <div class="mt-2 d-flex gap-2">
          <button class="btn btn-danger" @click="onGamesDelete(item)">
            <i class="bi bi-trash"></i> Удалить
          </button>
          <button
            class="btn btn-primary"
            @click="onGamesEdit(item)"
            data-bs-toggle="modal"
            data-bs-target="#editGamesModal"
          >
            <i class="bi bi-pencil"></i> Редактировать
          </button>
        </div>
      </div>
    </div>

    <div class="mt-3">
      <button class="btn btn-secondary" @click="fetchGames">Обновить список</button>
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
</template>

<style scoped>
.games-item {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
  display: block;
}

.mt-2.d-flex.gap-2 {
  display: flex;
  gap: 10px; 
}

.modal-dialog.modal-lg {
  max-width: 90%;
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
