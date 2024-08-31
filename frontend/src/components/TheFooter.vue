<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue'

const year = computed(() => {
  const date = new Date();
  return date.getFullYear() ;
});

</script>

<template>
  <footer>
    <div class="row">
      <div class="col">
        <RouterLink to="/">
          <img src="@/assets/logo_lg.png" class="logo_lg">
        </RouterLink>
        <p>Got stuck? Ask your question on Vue Land, our official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.</p>
      </div>
      <div class="col">
        <h3>Contact</h3>
        <p><strong>Adresse:</strong> 15944, Libreville, Gabon</p>
        <p><strong>Téléphone:</strong> +23456876199</p>
        <p><strong>Heures:</strong> 08.00 - 18.00, Lun - Sam</p>
        <h3>Suivez-nous</h3>
        <div class="icon">
          <a href="http://www.facebook.com/" target="_blank" class="social_media"><i class="fab fa-facebook"></i></a>
          <a href="http://www.instagram.com/" target="_blank" class="social_media"><i class="fab fa-instagram"></i></a>
          <a href="http://www.x.com/" target="_blank" class="social_media"><i class="fab fa-twitter"></i></a>
        </div>
      </div>
      <div class="col">
        <h3>Liens utiles</h3>
        <RouterLink to="/about">À propos</RouterLink>
        <RouterLink to="/product/all">Produits Disponibles</RouterLink>
        <a href="mailto:support@example.com?subject=Commande Spéciale //{produits}">Passer une Commande Spéciale</a>
        <RouterLink to="/about#pol_confid">Politique de Confidentialité</RouterLink>
        <RouterLink to="/about#cond_general">Conditions Générales</RouterLink>
      </div>
      <div class="col copyright">
        <p>&copy; {{ year }} Mes Achats en Chine. Tous droits réservés! </p>
      </div>
    </div>

</footer>
</template>

<style scoped>
footer {
  position: relative; 
  background-color: #E3E6F3;
  padding: 20px 15% 5px 15%;
  bottom: 0px;
}

.row {
  display: grid;
  gap: 20px;
  width: 100%;
}

footer a {
  display: flex;
  font-size: 16px;
  text-decoration: none;
  color: #465b52;
  line-height: 24px;
} 

footer p {
  font-size: 16px;
  line-height: 24px;
  margin: 0px 0 0px 0
}

.logo_lg {
  height:32px;
}

footer .icon .social_media {
  display: inline;
  color: #465b52;
  padding: 7px 10px 7px 10px;
  margin-right: 5px;
  cursor: pointer;
  border: 1px solid var(--color-border);
  border-radius: 10%;
}

footer i:hover, footer a:hover {
  color: #088178;
 
}
.copyright{
    text-align: center
}
@media(min-width: 780px) {
  .row {
    grid-template-columns: 1fr 1fr;
  }
  .row :first-child {
    grid-column-end: span 2;
  }
  .row :last-child {
    grid-column-end: span 2;
  }
}


@media (max-width: 920px) {
  footer{
    padding: 20px 10% 5px 10%;
  }

}

@media (max-width: 477px) {
  footer{
    padding: 10px 5% 5px 5%;
  }

  footer a {
  font-size: 12px;
} 

footer p {
  font-size: 12px;
}

}
</style>
