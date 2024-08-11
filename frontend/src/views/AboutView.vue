<template>
  <section id="about">
    <div class="container">

      <div class="about-part-1">
        <div class="about-img">
          <img src="https://i.ibb.co/QP6Nmpf/image-1-about.jpg" loading="lazy" alt="A propos de mes achats en chine">
        </div>
      </div>

      <div class="about-part-2">
        <div class="about-content">
          <h2>À Propos De Nous</h2>
          <h3>Bienvenu(e) sur Mes Achats en Chine.</h3>
          <p>Si vous êtes arrivé jusque là, c'est sans doute parce que vous voulez savoir ce que nous faisons, pourquoi nous le faisons, et par ricochet, savoir à qui vous avez affaire.</p>
          <h3>Pour faire court...</h3>
          <p>Mon nom est Yves Fidèle, je suis le fondateur de Mes Achats en Chine. Tout a commencé en 2020, une année marquée par une crise sanitaire mondiale et par des confinements. Le télétravail ayant désormais pris de plus en plus grandes proportions, je passais alors beaucoup de temps sur internet à me renseigner sur comment avoir des revenus grâce à internet. Plusieurs options se sont offertes à moi. Au vu des compétences que j'avais déjà, j'ai opté pour le freelancing. Il me faut maintenant me faire connaitre et toucher un public susceptible d'être intéressé par mes services et faire le nécessaire pour que mes clients soient satisfaits.
          </p>
          <h3>Mais alors, où se situe le problème ?</h3>
          <ul>
            <li><i class="ion-android-checkmark-circle"></i> Où poster mes services sans rien devoir, afin de débuter ?</li>
            <li><i class="ion-android-checkmark-circle"></i> Comment les promouvoir ?</li>
            <li><i class="ion-android-checkmark-circle"></i> Comment cibler le public adéquat ?</li>
          </ul>
        </div>
      </div>

    </div>
  </section><!-- #about -->

  <section id="why-us">          
    <div class="why-us-content">
      <div class="features">
        <i class="fa fa-diamond" style="color: #f058dc;"></i>
        <h4>Publication d'articles</h4>
        <p>Assurer la modération et une large diffusion de vos articles, de diverses thématiques</p>
      </div>
      <div class="features">
        <i class="fa fa-object-group" style="color: #ffb774;"></i>
        <h4>Espace d'annonces</h4>
        <p>Promouvoir les produits et services en mettant en contact l'annonceur et les potentiels clients</p>
      </div>
      <div class="features">
        <i class="fa fa-tag" style="color: #589af1;"></i>
        <h4>Marketing</h4>
        <p>Favoriser l'augmentation du trafic sur l'ensembles de vos articles, services et produits</p>
      </div>
    </div>

    <div class="container">
      <div class="item text-center">
        <span data-toggle="counter-up">23</span>
        <p>Clients</p>
      </div>
      <div class="item text-center">
        <span data-toggle="counter-up">02</span>
        <p>Articles</p>
      </div>
      <div class="item text-center">
        <span data-toggle="counter-up">67</span>
        <p>Services</p>
      </div>
      <div class="item text-center">
        <span data-toggle="counter-up">90</span>
        <p>Profils</p>
      </div>
    </div>

  </section>

</template>


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