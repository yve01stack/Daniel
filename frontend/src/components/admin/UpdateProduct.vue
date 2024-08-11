<template>
    <ProductFilter 
      :categories="productCategories" 
      :availabilities="countryList" 
      @queryData="handleQuery"/>
    
    <section class="pro-container">
        <div class="card-container">
            <div class="card" v-for="product in displayedProducts" @click="selectItem(product)">
                <img :src="product.imgSrc" :alt="product.title">
                <div class="card-content">
                    <el-tooltip :content="product.title" placement="bottom" effect="light">
                        <h3>{{product.title}}</h3>
                    </el-tooltip>
                    <p class="price">{{product.price}} {{ product.currency }}</p>
                    <div class="rating">
                        <el-rate
                            v-model="product.rating"
                            disabled
                            text-color="#ff9900"
                        />
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="button-container">
      <el-button @click="seeMore" size="large" round :disabled="allProductsDisplayed">Voir Plus+</el-button>
    </div>
    
    <!-- add product form dialog -->
    <el-dialog v-model="updateProductDialog" width="400" draggable>
        <template #header="{titleId, titleClass }">
            <div>
                <h3 :id="titleId" :class="titleClass">Mettre à jour du produit</h3>
            </div>
        </template>        
        <el-form :model="productForm" label-width="auto" width="400" label-position="top">
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
                        <img v-if="photo.type === 'image'" :src="photo.src" alt="photo" class="photo"  />
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
                <el-button @click="updateProductDialog = false">Annuler</el-button>
                <el-button type="primary" @click="updateProduct">Mettre à Jour</el-button>
            </div>
        </template>
    </el-dialog>

    <el-dialog v-model="photoPreviewDialog" width="400">
        <img v-if="photoPreviewUrl.type === 'image'" 
        :src="photoPreviewUrl.src" alt="Preview Image" class="media_preview" />
        <video v-else ref="previewVideo" @click="togglePlayPause" autoplay class="media_preview">
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
import { ref, reactive, computed, toRaw  } from 'vue'
import { Plus, Delete, ZoomIn } from '@element-plus/icons-vue'
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';
import HtmlEditor from '../HtmlEditor.vue';
import ProductFilter from '../ProductFilter.vue'
  
const store = useStore();

const products = computed(() => store.getters['product/products']);
const unique_categories = computed(() => store.getters['product/categories']);
const availabilities = computed(() => store.getters['product/availabilities']);

const productForm = reactive({
    prodId: '',
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

const updateProductDialog = ref(false);

const selectItem = (selected) => {
    productForm.prodId = selected.id
    productForm.itemId = selected.itemId
    productForm.category = selected.category
    productForm.storeTitle = selected.storeTitle
    productForm.title = selected.title
    productForm.rating = selected.rating
    productForm.desc = selected.desc
    productForm.imgSrc = selected.imgSrc
    productForm.price = selected.price
    productForm.currency = selected.currency
    productForm.available_in = selected.available_in
    productForm.media = selected.media
    // open the dialog
    updateProductDialog.value = true;
};

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

const updateProduct = async () => {
    
    const form = toRaw(productForm);

    await store.dispatch('admin/updateProduct', form)
    .then((data) => {
        if (data.status === 'success') {
            ElMessage({type: 'success', message: data.message})
            updateProductDialog.value = false;
            fetchProducts();
        } else {
            ElMessage({type: 'error', message: data.message})
        }
    })
};


// filter and display products
const productCategories = computed(() => {
// Step 1: Extract unique categories
const uniqueCategories = [...new Set(products.value.map(product => product.category))];
// Step 2: Transform into the desired format
const categoryList = uniqueCategories.map(category => ({
    value: category,
    label: category
}));

return categoryList;
});

const countryList = computed(() => {
// Flatten the available_in arrays into one unique countries array
const uniqueCountries = [...new Set(products.value.flatMap(product => product.available_in))];
const countryList = uniqueCountries.map(country => ({
    value: country,
    label: country
}));

return countryList;
});

const filterAndSortProducts = (products, filterQuery) => {
return products.value
    .filter((product) => {
    // Filter by query (title and description)
    const query = filterQuery.query.toLowerCase();
    if (query) {
        const titleMatches = product.title.toLowerCase().includes(query);
        if (!titleMatches) {
        return false;
        }
    }

    // Filter by category
    if (filterQuery.category.length && !filterQuery.category.includes(product.category)) {
        return false;
    }

    // Filter by availability in countries
    if (filterQuery.available_in.length) {
        const availableInMatch = filterQuery.available_in.some(country => product.available_in.includes(country));
        if (!availableInMatch) {
        return false;
        }
    }

    return true;
    })
    .sort((a, b) => {
    // Sort by specified criteria
    if (filterQuery.sortBy === 'price') {
        return a.price - b.price;
    } else if (filterQuery.sortBy === 'rating') {
        return b.rating - a.rating;
    }
    return 0; // No sorting if no valid sortBy value
    });
};

// See more button
const productsPerPage = 10;
const displayedCount = ref(productsPerPage);

let filteredProducts = products.value;
const handleQuery = (filterQuery) => {
filteredProducts = filterAndSortProducts(products, filterQuery);
displayedCount.value = productsPerPage;
seeMore()
};

const displayedProducts = computed(() => {
return filteredProducts.slice(0, displayedCount.value);
});

const allProductsDisplayed = computed(() => {
return displayedCount.value >= filteredProducts.length;
});

const seeMore = () => {
displayedCount.value += productsPerPage;
};


const fetchProducts = async () => {
    await store.dispatch('product/fetchProducts');
    products.value = computed(() => store.getters['product/products']);
};

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

.button-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
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
  