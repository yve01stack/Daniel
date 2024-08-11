<template>
    <el-form  :inline="true" :model="formSearch">
        <el-form-item>
            <el-select 
            v-model="formSearch.group" 
            placeholder="Type" 
            style="width: 200px;"
            >
                <el-option
                v-for="item in categories"
                :key="item.name"
                :label="item.name"
                :value="item.name"
                />
            </el-select>
        </el-form-item>
        <el-form-item>
            <el-select 
            v-model="formSearch.category" 
            placeholder="Catégorie" 
            style="width: 200px;"
            >
                <el-option
                v-for="item in selectedGroup"
                :key="item.name"
                :label="item.name"
                :value="item.name"
                />
            </el-select>
        </el-form-item>
        <el-form-item>
            <el-input
                v-model="formSearch.query"
                style="width: 200px;"
                placeholder="Recherche..."
            >
                <template #suffix>
                    <el-button link style="margin-right: -5px;" @click="searchForm" :icon="Search" />
                    <el-tooltip effect="light" content="Ajouter un produit manuellement" placement="top">
                        <el-button size="small" type="primary" style="margin-right: -6px;" @click="manuallyAddNewProduct" :icon="Plus"></el-button>
                    </el-tooltip>
                </template>
            </el-input>
        </el-form-item>
    </el-form>
    
    <div class="card-container">
        <div class="card" v-for="product in searchItems" @click="selectItem(product.item)">
            <img :src="product.item.image" :alt="product.item.title">
            <div class="card-content">
                <el-tooltip :content="product.item.title" placement="bottom" effect="light">
                    <h3>{{product.item.title}}</h3>
                </el-tooltip>
                <p class="price">${{product.item.sku.def.promotionPrice}}</p>
                <div class="rating">
                    <el-rate
                        v-model="product.item.averageStarRate"
                        disabled
                        text-color="#ff9900"
                    />
                </div>
            </div>
        </div>
    </div>

    <!-- add product form dialog -->
    <el-dialog v-model="addProductDialog" width="400" draggable>
        <template #header="{titleId, titleClass }">
            <div>
                <h3 :id="titleId" :class="titleClass">Ajouter un nouveau produit</h3>
            </div>
        </template>        
        <el-form :model="productForm" label-width="auto" label-position="top">
            <el-form-item label="Image principale">
                <el-input v-model="productForm.imgSrc" autocomplete="off" />
            </el-form-item>
            <el-form-item label="Titre du produit">
                <el-input v-model="productForm.title" autocomplete="off" type="textarea" 
                :autosize="{ minRows: 2, maxRows: 4 }"/>
            </el-form-item>
            <el-form-item label="Catégorie">
                <el-select
                v-model="productForm.category"
                filterable
                allow-create
                default-first-option
                :reserve-keyword="false"
            >
                    <el-option v-for="category in unique_categories" :label="category" :value="category"/>
                </el-select>
            </el-form-item>
            <el-form-item label="Boutique">
                <el-input v-model="productForm.storeTitle" />
            </el-form-item>
            <el-form-item label="Prix">
                <el-col :span="11">
                    <el-input
                    v-model="productForm.price"
                    type="number"
                    placeholder="Montant"
                    style="width: 100%"
                    />
                </el-col>
                <el-col :span="2" style="text-align: center; color: gray;">
                    <span >-</span>
                </el-col>
                <el-col :span="11">
                    <el-select
                    v-model="productForm.currency"
                    filterable
                    allow-create
                    default-first-option
                    :reserve-keyword="false"
                    placeholder="Unité monétaire"
                    style="width: 100%"
                    >
                        <el-option label="Fcfa" value="Fcfa"/>
                        <el-option label="USD" value="USD"/>
                        <el-option label="EUR" value="EUR"/>
                    </el-select>
                </el-col>
            </el-form-item>
            <el-form-item label="Disponible en"> 
                <el-select
                v-model="productForm.available_in"
                multiple
                filterable
                allow-create
                default-first-option
                :reserve-keyword="false"
            >
                    <el-option v-for="country in availabilities" :label="country" :value="country"/>
                </el-select>
            </el-form-item>
            <el-form-item label="Notation"> 
                <el-rate v-model="productForm.rating" />
            </el-form-item>
            <el-form-item label="Description"> 
                <el-input v-model="productForm.desc" type="textarea" 
                :autosize="{ minRows: 2, maxRows: 6 }"/>
                <!-- <HtmlEditor v-model="productForm.desc" /> -->
            </el-form-item>
            <el-form-item label="Médias">
                <div class="photo-wall">
                    <div class="photo-item"
                    v-for="(photo, index) in productForm.media" 
                    :key="index"
                    @mouseover="hoveredPhoto = index"
                    @mouseleave="hoveredPhoto = null"
                    >
                        <img v-if="photo.type === 'image'" :src="photo.src" alt="Photo" class="photo"  />
                        <video v-else class="photo">
                            <source :src="photo.src" type="video/mp4" alt="vidéo"/>
                        </video>
                        <img/>
                        <div class="overlay" v-if="hoveredPhoto === index">
                            <el-button :icon="ZoomIn" style="color: aliceblue; font-size: large;" link @click="zoomPhoto(photo)" />
                            <el-button :icon="Delete" style="color: aliceblue; font-size: large;" link @click="removePhoto(index)" />
                        </div>
                    </div>
                    <div class="photo-new-item" @click="addNewMediaDialog = true">
                        <el-icon><Plus /></el-icon>
                    </div>
                </div>
            </el-form-item>     
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addProductDialog = false">Annuler</el-button>
                <el-button type="primary" @click="addProduct">Ajouter</el-button>
            </div>
        </template>
    </el-dialog>

    <el-dialog v-model="photoPreviewDialog" width="400" draggable>
        <img v-if="photoPreviewUrl.type === 'image'" 
        :src="photoPreviewUrl.src" alt="Preview Image" class="media_preview" />
        <video v-else ref="previewVideo" @click="togglePlayPause" autoplay class="media_preview" id="video_controls">
            <source :src="photoPreviewUrl.src" type="video/mp4" />
        </video>
    </el-dialog>

    <el-dialog v-model="addNewMediaDialog" width="400" draggable>
        <template #header="{titleId, titleClass }">
            <div>
                <h3 :id="titleId" :class="titleClass">Ajouter une photo/vidéo</h3>
            </div>
        </template>        
        <el-form :model="mediaForm" label-width="auto" label-position="top">
            <el-form-item label="Média type"> 
                <el-select
                v-model="mediaForm.type"     
                default-first-option
                :required="true"
            >
                    <el-option label="Image" value="image"/>
                    <el-option label="Vidéo" value="video"/>
                </el-select>
            </el-form-item>
            <el-form-item label="Url">
                <el-input v-model="mediaForm.src" :required="true" type="url"/>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addProductDialog = false">Annuler</el-button>
                <el-button type="primary" @click="addNewMedia">Ajouter</el-button>
            </div>
        </template>
    </el-dialog>
</template>
  
<script setup>
import { ref, reactive, computed, onMounted, toRaw  } from 'vue'
import { Search, Delete, ZoomIn, Plus } from '@element-plus/icons-vue'
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';
import HtmlEditor from '../HtmlEditor.vue';


const store = useStore();

const categories = computed(() => store.getters['admin/categories']);
const searchItems = computed(() => store.getters['admin/searchItems']);
const item = computed(() => store.getters['admin/item']);
const unique_categories = computed(() => store.getters['product/categories']);
const availabilities = computed(() => store.getters['product/availabilities']);

const formSearch = reactive({
    group: '',
    query: '',
    category: '',
})

const selectedGroup = computed(() => {
    if (formSearch.group !== '') {
        let list = categories.value.filter(item => item.name === formSearch.group);
        return list[0].list;
    } else return [];

});

const searchForm = async () => {
    const form = {group: formSearch.group, query: formSearch.query, category: formSearch.category}
    await store.dispatch('admin/aliSearch', form); 
};

const productForm = reactive({
    itemId: '',
    category: '',
    storeTitle: '',
    title: '',
    rating: 0,
    desc: '',
    imgSrc: '',
    price: '',
    currency: '',
    available_in: [],
    media: [{}],
})

const addProductDialog = ref(false);
const selectedItem = ref({});

const selectItem = async (selected) => {
    await store.dispatch('admin/aliProduct', {itemId: selected.itemId})
    .then((data)=>{
        if (data.status == 'success') {
            selectedItem.value = selected.itemId;
            // update productForm
            let category = '';

            if (item.value.breadcrumbs) {
                if (item.value.breadcrumbs.length > 0) {
                    category = item.value.breadcrumbs[0].title;
                } 
            }

            let media = [];
            item.value.images.forEach(image => {
                media.push({ 'type': 'image', 'src': image });
            });

            if (item.value.video) {
                if (item.value.video.url){
                    media.push({ 'type': 'video', 'src': item.value.video.url });
                }
            }

            const extractTextFromHTML = (htmlString) => {
                const tempElement = document.createElement('div');
                // Set the innerHTML to the provided HTML string
                tempElement.innerHTML = htmlString;
                // Extract the text content
                const textContent = tempElement.textContent || tempElement.innerText || "";
                return textContent.trim();
            }

            productForm.desc = extractTextFromHTML(item.value.description.html);

            productForm.itemId = item.value.itemId
            productForm.category = category
            productForm.storeTitle = item.value.storeTitle
            productForm.title = item.value.title
            productForm.rating = selected.averageStarRate
            productForm.imgSrc = selected.image
            productForm.price = selected.sku.def.promotionPrice
            productForm.currency = 'USD'
            productForm.available_in = []
            productForm.media = media
            // open the dialog
            addProductDialog.value = true;
        } else {
            ElMessage({message: data.message, type: 'error'})
        }
    })
};

const manuallyAddNewProduct = () => {
    productForm.itemId = Date.now();
    productForm.imgSrc = '';
    productForm.category = '',
    productForm.storeTitle = '';
    productForm.title = '';
    productForm.rating = 0;
    productForm.desc = '';
    productForm.price = '';
    productForm.currency = 'Fcfa';
    productForm.available_in = [];
    productForm.media = [{}];
    addProductDialog.value = true;
}

const hoveredPhoto = ref(null);
const removePhoto = (index) => {
    productForm.media.splice(index, 1);
};

const photoPreviewDialog = ref(false)
const photoPreviewUrl = ref({})

const zoomPhoto = (photo) => {
    photoPreviewUrl.value = photo;
    photoPreviewDialog.value = true;
};

const previewVideo = ref(null);

const togglePlayPause = () => {
  const video = previewVideo.value;
  if (video.paused) {
    video.play();
  } else {
    video.pause();
  }
};

const mediaForm = reactive({
    type: '',
    src: '',
})

const addNewMediaDialog = ref(false);

const addNewMedia = () => {
    const media = toRaw(mediaForm);
    productForm.media.push({type: media.type, src: media.src});
    addNewMediaDialog.value = false
}

const addProduct = async () => {

    const form = toRaw(productForm);

    await store.dispatch('admin/addProduct', form)
    .then((data) => {
        if (data.status === 'success') {
            ElMessage({type: 'success', message: data.message})
            addProductDialog.value = false;
        } else {
            ElMessage({type: 'error', message: data.message})
        }
    })
};



const fetchCategories = async () => {
  await store.dispatch('admin/aliCategory');
};

onMounted(() => {
    fetchCategories();
});

</script>

<style scoped>
.el-form--inline .el-form-item {
  margin-right: 8px ;
  margin-bottom: 8px;
}

:deep(.el-rate) {
  margin-top: -8px;
  margin-bottom: -8px;
}

:deep(.el-rate__item) {
  margin-right: -8px;
} 

.photo-wall {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.photo-item {
  position: relative;
  width: 100px;
  height: 100px; 
}

.photo-new-item{
    position: relative;
    width: 100px;
    height: 100px;
    border: 1px solid rgb(210, 210, 210);
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 28px;    
}

.photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.photo-item:hover .overlay {
  opacity: 1;
}

.el-button {
  margin: 0 3px;
}

.media_preview {
    position: relative;
    width: 100%;
    height: 100%;
}

#video_controls {
    cursor: pointer;
}

/* Search result card */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.card {
  background: #fff;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  width: 23%;
  margin: 3px;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-4px);
}

.card img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

.card-content {
  padding: 8px;
}

.card-content h3 {
  font-size: 14px;
  color: #333;
  font-weight: 600;
  line-height: 18px;
  height: 35px;
  overflow: hidden;
  /* white-space: nowrap; */
  /* text-overflow: ellipsis; */
}

.card-content .price {
  font-size: 16px;
  color: #e74c3c;
  margin: 0px 0;
}

@media (max-width: 1080px) {
    .card {
        width: 30%;
    }
}

@media (max-width: 630px) {
    .card {
        width: 30%;
    }

    .card-content h3 {
        font-size: 12px;
        /* font-weight: 600; */
    }

    .card-content .price {
        font-size: 14px;
    }
}

@media (max-width: 477px) {
    .card {
        width: 44%;
    }
}
</style>
  