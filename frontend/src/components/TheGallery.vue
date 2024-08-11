<template>
    <div>
      <div class="thumbnail-grid">
        <div v-for="(media, index) in medias" :key="media.id" class="thumbnail" @click="openGallery(index)">
          <img v-if="isImage(media)" :src="media.src" alt="Product Image" />
          <video v-else>
            <source :src="media.src" type="video/mp4" />
          </video>
          <div class="play-icon"></div>
        </div>
      </div>
  
      <div v-if="isGalleryOpen" class="lightbox" @click="closeGallery">
        <div class="lightbox-content" @click.stop>
          <button class="close-button" @click="closeGallery">
            <i class="fas fa-times"></i>
          </button>
          <button class="prev-button" @click="prevMedia">
            <i class="fas fa-chevron-left"></i>          
          </button>
          <div>
            <img v-if="isImage(currentMedia)" :src="currentMedia.src" alt="Product Image" />
            <video v-else autoplay ref="previewVideo" @click="togglePlayPause">
              <source :src="currentMedia.src" type="video/mp4" />
            </video>
          </div>
          <button class="next-button" @click="nextMedia">
            <i class="fas fa-chevron-right"></i>          </button>
        </div>
      </div>
    </div>
   
  </template>
  
  <script setup>
  import { ref, defineProps } from 'vue';
  
  const props = defineProps({
    medias: { type: Object, required: true }
  })
  
  const isGalleryOpen = ref(false);
  const currentIndex = ref(0);
  
  const currentMedia = ref(props.medias[currentIndex.value]);
  
  const isImage = (media) => media.type === 'image';
  
  const openGallery = (index) => {
    currentIndex.value = index;
    currentMedia.value = props.medias[currentIndex.value];
    isGalleryOpen.value = true;
  };
  
  const closeGallery = () => {
    isGalleryOpen.value = false;
  };
  
  const prevMedia = () => {
    if (currentIndex.value > 0) {
      currentIndex.value--;
    } else {
      currentIndex.value = props.medias.length - 1;
    }
    currentMedia.value = props.medias[currentIndex.value];
  };
  
  const nextMedia = () => {
    if (currentIndex.value < props.medias.length - 1) {
      currentIndex.value++;
    } else {
      currentIndex.value = 0;
    }
    currentMedia.value = props.medias[currentIndex.value];
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

  </script>
  
  <style scoped>
  .thumbnail-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .thumbnail {
    cursor: pointer;
    max-width: 90px;
    max-height: 65px;
    overflow: hidden;
    position: relative;
    display: inline-block;
    border-radius: 10%;
    border: 2px solid whitesmoke;
  }
  
  .thumbnail img,
  .thumbnail video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  
  .play-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 28px;
    height: 28px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    }

  .play-icon::before {
    content: '';
    display: block;
    width: 0;
    height: 0;
    border-left: 14px solid white;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
  }

  .lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .lightbox-content {
    position: relative;
    max-width: 70%;
    max-height: 70%;
    text-align: center;
  }
  
  .lightbox img,
  .lightbox video {
    max-width: 100%;
    max-height: 100%;
  }
  
  .close-button,
  .prev-button,
  .next-button {
    position: absolute;
    background: none;
    border: none;
    color: white;
    font-size: 2em;
    cursor: pointer;
  }
  
  .close-button {
    top: 10px;
    right: 10px;
  }
  
  .prev-button {
    top: 50%;
    left: 10px;
    transform: translateY(-50%);
  }
  
  .next-button {
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
  }

  @media (max-width: 900px) {
    .lightbox-content {
      max-width: 80%;
      max-height: 80%;
    }
  }

  @media (max-width: 477px) {
    .lightbox-content {
      max-width: 100%;
      max-height: 100%;
    }
  }
  </style>
  