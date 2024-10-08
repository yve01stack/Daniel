<template>
  <section id="about">
    <div class="container">

      <div class="about-part-1">
        <div class="about-img">
          <img src="@/assets/image-1-about.jpg" loading="lazy" alt="A propos de mes achats en chine">
        </div>
      </div>

      <div class="about-part-2">
        <div class="about-content">
          <h2>À Propos de Mes Achats en Chine</h2>
          <p>est une plateforme fondée par <b>Daniel Nehemy</b>, spécialisée dans l'exportation de produits de Chine vers le monde entier, y compris en <b>Afrique</b> et en <b>Europe</b>. Notre mission est simple : offrir aux clients la possibilité de commander des produits, en gros ou en détail, directement auprès des meilleurs fournisseurs chinois, tout en garantissant <b>le meilleur prix du marché</b> et <b>la sécurité des transactions</b>.</p>
          <p>En nous appuyant sur un réseau de partenaires fiables et expérimentés en Chine, nous nous assurons que chaque produit commandé est soigneusement sélectionné, emballé, et expédié dans des conditions optimales. Nous prenons en charge l'intégralité du processus logistique, depuis la commande jusqu'à la livraison à votre porte.</p>
        </div>
      </div>

    </div>
  </section><!-- #about -->

  <section id="why-us">          
    <div class="why-us-content">
      <div id="about">
        <div class="about-content">
          <h3>Pour faire court...</h3>
          <p>Aujourd'hui, nous sommes fiers de compter de nombreux clients satisfaits dans des pays tels que la France, le Gabon, le Togo, le Bénin, la Côte d'Ivoire, le Cameroun, et le Congo. Notre expertise et notre engagement à fournir des produits de qualité au meilleur prix nous permettent de répondre aux besoins des entreprises comme des particuliers, en toute confiance.</p>
        </div>
      </div> 

      <div class="features">
        <i class="fa fa-diamond" style="color: #f058dc;"></i>
        <h4>Politique de Confidentialité</h4>
        <p>Nous prenons la <b>confidentialité de vos informations personnelles très au sérieux</b>. Toutes les données collectées sur notre site sont traitées de manière sécurisée, conformément aux lois et réglementations en vigueur. Nous nous engageons à ne jamais vendre, louer ou partager vos informations à des tiers sans votre consentement explicite. Pour plus de détails, veuillez consulter notre <b>Politique de Confidentialité complète</b>.</p>
      </div>
      <div class="features">
        <i class="fa fa-object-group" style="color: #ffb774;"></i>
        <h4>Conditions Générales d'Utilisation</h4>
        <p>En utilisant <b>Mes Achats en Chine</b>, vous acceptez de respecter nos <b>Conditions Générales d'Utilisation</b>, qui régissent toutes les transactions effectuées sur notre plateforme. Cela inclut les modalités de paiement, la gestion des retours, ainsi que nos règles relatives aux droits des consommateurs. Nous mettons tout en œuvre pour garantir une transparence totale tout au long du processus d'achat.</p>
      </div>
      <div class="features">
        <i class="fa fa-tag" style="color: #589af1;"></i>
        <h4>Pourquoi Choisir Mes Achats en Chine ?</h4>
        <p><i class="fa fa-check-double" style="color: #088178; font-size:larger; padding-right: 5px;"></i><b>Meilleurs prix garantis</b>: Nous négocions directement avec les fournisseurs pour vous offrir des tarifs imbattables.</p>
        <p><i class="fa fa-check-double" style="color: #088178; font-size:larger; padding-right: 5px;"></i><b>Sécurité</b>: Vos transactions sont 100% sécurisées, avec un suivi rigoureux des commandes.</p>
        <p><i class="fa fa-check-double" style="color: #088178; font-size:larger; padding-right: 5px;"></i><b>Service client dédié</b>: Notre équipe est disponible pour répondre à toutes vos questions et vous accompagner tout au long de votre expérience d'achat.</p>
        <p>Rejoignez dès aujourd'hui <b>Mes Achats en Chine</b>, votre passerelle vers des achats intelligents et sécurisés directement depuis la Chine !</p>
      </div>
    </div>

    <div class="container">
      <div class="item text-center">
        <span data-toggle="counter-up">{{ dashboard.statistic[0].value }}</span>
        <p>Clients</p>
      </div>
      <div class="item text-center">
        <span data-toggle="counter-up">{{ dashboard.statistic[5].value }}</span>
        <p>Commandes</p>
      </div>
      <div class="item text-center">
        <span data-toggle="counter-up">18</span>
        <p>Fournisseurs</p>
      </div>
      <div class="item text-center">
        <span data-toggle="counter-up">{{ dashboard.statistic[1].value }}</span>
        <p>Produits</p>
      </div>
    </div>

  </section>

</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore()

const dashboard = computed(() => store.getters['admin/dashboard']);

const fetchDashboard = async () => {
    await store.dispatch('admin/fetchDashboard');
};

onMounted(() => {
    fetchDashboard();
});  

</script>

<style scoped>

/* About Us Section
--------------------------------*/
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
}

#about .about-part-1 {
  width: 54%;
}

#about .about-part-2 {
  width: 42%;
}

#about .about-content {
  padding-top: 40px;
}

#about .about-content h2 {
  color: #413e66;
  font-family: "Montserrat", sans-serif;
  font-weight: 700;
}

#about .about-content h3 {
  color: #696592;
  font-weight: 400;
  font-size: 22px;
  font-style: italic;
}

#about .about-content ul {
  list-style: none;
  padding: 0;
}

#about .about-content ul li {
  padding-bottom: 10px;
}

#about .about-content ul li i {
  font-size: 20px;
  padding-right: 4px;
  color: #1bb1dc;
}

#about .about-img {
  position: relative;
  margin: 30px 30px 30px 30px;
}

#about .about-img img {
  width: 100%;
  border: 8px solid #fff;
  transition: .5s;
}

#about .about-img img:hover {
  width: 100%;
  -webkit-transform: scale(1.03);
  transform: scale(1.03);
}

#about .about-img::before {
  position: absolute;
  left: -31px;
  top: -30px;
  width: 90%;
  height: 92%;
  z-index: -1;
  content: '';
  background-color: #ebf1fa;
  transition: .5s;
}

#about .about-img::after {
  position: absolute;
  right: -31px;
  bottom: -30px;
  width: 90%;
  height: 92%;
  z-index: -1;
  content: '';
  background-color: #ebf1fa;
  transition: .5s;
}

/* Why Us Section
--------------------------------*/

#why-us {
  padding: 20px 0;
}

#why-us .why-us-content .features {
  margin: 0 0 15px 0;
  padding: 0;
  transition: 0.3s ease-in-out;
}

#why-us .why-us-content .features i {
  font-size: 36px;
  float: left;
}

#why-us .why-us-content .features h4 {
  font-size: 24px;
  font-weight: 600;
  margin-left: 56px;
  color: #413e66;
  margin-bottom: 5px;
}

#why-us .why-us-content .features p {
  font-size: 16px;
  margin-left: 56px;
  color: #555186;
}

/* Section counters
--------------------------------*/
#why-us .container {
  padding-top: 40px;
  justify-content: center;
}

#why-us .container .item {
  width: 23%;
  text-align: center;
}

#why-us .container .item span {
  font-family: "Montserrat", sans-serif;
  font-weight: bold;
  font-size: 48px;
  display: block;
  color: #555186;
}

#why-us .container .item p {
  padding: 0;
  margin: 0 0 20px 0;
  font-family: "Montserrat", sans-serif;
  font-size: 14px;
  color: #8a87b6;
}


@media (max-width: 1200px) {
  #about .about-part-1, #about .about-part-2 {
    width: 48%;
  }

}

@media (max-width: 700px) {
  #about .about-part-1, #about .about-part-2{
    width: 100%;
  }

  #why-us .container .item {
    width: 48%;
  }
}

</style>