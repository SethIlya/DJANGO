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

const statistics = ref({
  mostProductiveStudio: '',
  mostPopularGenre: '',
  mostProductiveDirector: '',
  mostPopularPlatform: ''
});

const gamesPictureRef = ref(null);
const gamesAddImageUrl = ref('');
const editPictureRef = ref(null);
const editImageUrl = ref('');
const viewImageUrl = ref(''); 

// Поля для фильтрации
const filterName = ref('');
const filterStudio = ref('');
const filterGenre = ref('');
const filterDirector = ref('');
const filterPlatform = ref('');

// Храним комментарии для каждой игры
const commentsByGameId = ref({});
// Поле для нового комментария для каждой игры
const newCommentText = ref({});

onMounted(() => {
  const csrfToken = Cookies.get('csrftoken');
  if (csrfToken) {
    axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  } else {
    console.warn('CSRF токен не найден.');
  }
});

// Загрузка игр с учётом фильтров
async function fetchGames() {
  try {
    let url = "/api/games/?";
    const params = [];

    if (filterName.value) {
      params.push(`name=${encodeURIComponent(filterName.value)}`);
    }
    if (filterStudio.value) {
      params.push(`studio=${encodeURIComponent(filterStudio.value)}`);
    }
    if (filterGenre.value) {
      params.push(`genre=${encodeURIComponent(filterGenre.value)}`);
    }
    if (filterDirector.value) {
      params.push(`director=${encodeURIComponent(filterDirector.value)}`);
    }
    if (filterPlatform.value) {
      params.push(`platform=${encodeURIComponent(filterPlatform.value)}`);
    }

    url += params.join('&');

    const response = await axios.get(url);
    games.value = response.data;

    // Загрузим комментарии для каждой игры
    for (let g of games.value) {
      await fetchCommentsForGame(g.id);
    }
  } catch (error) {
    console.error('Ошибка при получении игр:', error);
  }
}

async function fetchCommentsForGame(gameId) {
  try {
    const response = await axios.get(`/api/games/${gameId}/comments/`);
    commentsByGameId.value[gameId] = response.data; // последние 4 комментария
  } catch (error) {
    console.error(`Ошибка при получении комментариев для игры ${gameId}:`, error);
  }
}

async function addComment(gameId) {
  const text = newCommentText.value[gameId] || '';
  if (!text.trim()) {
    alert("Введите текст комментария");
    return;
  }

  try {
    const response = await axios.post(`/api/games/${gameId}/comments/`, { text });
    // Добавляем новый комментарий в начало массива
    if (!commentsByGameId.value[gameId]) {
      commentsByGameId.value[gameId] = [];
    }
    commentsByGameId.value[gameId].unshift(response.data);

    // Если теперь стало >4 комментариев, обрежем массив
    if (commentsByGameId.value[gameId].length > 4) {
      commentsByGameId.value[gameId].pop();
    }

    newCommentText.value[gameId] = ''; // очистим поле ввода
  } catch (error) {
    console.error('Ошибка при добавлении комментария:', error);
    if (error.response && error.response.status === 403) {
      alert("Требуется авторизация, чтобы оставить комментарий.");
    }
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

async function fetchStatistics() {
  try {
    const response = await axios.get("/api/games/statistics/");
    statistics.value.mostProductiveStudio = response.data.most_productive_studio;
    statistics.value.mostPopularGenre = response.data.most_popular_genre;
    statistics.value.mostProductiveDirector = response.data.most_productive_director;
    statistics.value.mostPopularPlatform = response.data.most_popular_platform;
  } catch (error) {
    console.error('Ошибка при получении статистики:', error);
  }
}

onBeforeMount(async () => {
  await fetchGenres();
  await fetchStudios();
  await fetchDirectors();
  await fetchPlatforms();
  await fetchGames();
  await fetchStatistics();
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
    await fetchStatistics();
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
  if (!confirm(`Вы уверены, что хотите удалить игру "${game.name}"?`)) return;

  try {
    await axios.delete(`/api/games/${game.id}`);
    await fetchGames();
    await fetchStatistics();
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
    await fetchStatistics();
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

// Применить фильтры
async function applyFilters() {
  await fetchGames();
  await fetchStatistics();
}
</script>

<template>
  <div class="p-3 mb-4 border rounded">
    <h4>Статистика</h4>
    <div class="row g-3">
      <div class="col">
        <div class="card p-2">
          <b>Самая продуктивная студия по выпуску игр:</b> 
          <div>{{ statistics.mostProductiveStudio || 'Нет данных' }}</div>
        </div>
      </div>
      <div class="col">
        <div class="card p-2">
          <b>Самый популярный жанр игр:</b>
          <div>{{ statistics.mostPopularGenre || 'Нет данных' }}</div>
        </div>
      </div>
      <div class="col">
        <div class="card p-2">
          <b>Самый продуктивный режиссёр по выпуску игр:</b>
          <div>{{ statistics.mostProductiveDirector || 'Нет данных' }}</div>
        </div>
      </div>
      <div class="col">
        <div class="card p-2">
          <b>Самая популярная платформа:</b>
          <div>{{ statistics.mostPopularPlatform || 'Нет данных' }}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Фильтры -->
  <div class="p-3 mb-4 border rounded">
    <h4>Фильтры</h4>
    <div class="row gy-3 align-items-end">
      <div class="col-md-2">
        <label class="form-label">Имя игры</label>
        <input type="text" class="form-control" v-model="filterName" placeholder="Название">
      </div>
      <div class="col-md-2">
        <label class="form-label">Студия</label>
        <select class="form-select" v-model="filterStudio">
          <option value="">Все</option>
          <option :value="s.id" v-for="s in studios" :key="s.id">{{ s.name }}</option>
        </select>
      </div>
      <div class="col-md-2">
        <label class="form-label">Жанр</label>
        <select class="form-select" v-model="filterGenre">
          <option value="">Все</option>
          <option :value="g.id" v-for="g in genres" :key="g.id">{{ g.name }}</option>
        </select>
      </div>
      <div class="col-md-2">
        <label class="form-label">Режиссёр</label>
        <select class="form-select" v-model="filterDirector">
          <option value="">Все</option>
          <option :value="d.id" v-for="d in directors" :key="d.id">{{ d.name }} {{ d.surname }}</option>
        </select>
      </div>
      <div class="col-md-2">
        <label class="form-label">Платформа</label>
        <select class="form-select" v-model="filterPlatform">
          <option value="">Все</option>
          <option :value="p.id" v-for="p in platforms" :key="p.id">{{ p.name }}</option>
        </select>
      </div>
      <div class="col-12">
        <button class="btn btn-info" @click="applyFilters">Применить фильтр</button>
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
  </div>

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

  <!-- Список игр -->
  <div>
    <div v-for="item in games" :key="item.id" class="games-item mb-3 p-3 border rounded">
      <div class="row">
        <!-- Левая колонка: информация об игре -->
        <div class="col-8">
          <b>Название:</b> {{ item.name }} <br>
          <b>Жанр:</b> {{ genreById[item.genre]?.name }} <br>
          <b>Студия:</b> {{ studioById[item.studio]?.name }} <br>
          <b>Руководитель:</b> {{ directorById[item.director]?.name }} {{ directorById[item.director]?.surname }} <br>
          <b>Платформа:</b> {{ platformById[item.platform]?.name }} <br>

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

        <!-- Правая колонка: комментарии -->
        <div class="col-4">
          <h5>Комментарии</h5>
          <div v-if="commentsByGameId[item.id] && commentsByGameId[item.id].length > 0">
            <div 
              v-for="comment in commentsByGameId[item.id]" 
              :key="comment.id" 
              class="card mb-2"
            >
              <div class="card-body p-2">
                <strong>{{ comment.username }}:</strong><br>
                {{ comment.text }}
              </div>
            </div>
          </div>
          <div v-else>
            <div class="text-muted">Комментариев пока нет.</div>
          </div>

          <!-- Форма для добавления нового комментария -->
          <div class="mt-3">
            <input 
              type="text" 
              class="form-control mb-2" 
              :value="newCommentText[item.id]" 
              @input="newCommentText[item.id] = $event.target.value"
              placeholder="Ваш комментарий..."
            >
            <button class="btn btn-sm btn-secondary" @click="addComment(item.id)">Добавить комментарий</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="mt-3">
    <button class="btn btn-secondary" @click="() => { fetchGames(); fetchStatistics(); }">Обновить список</button>
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
