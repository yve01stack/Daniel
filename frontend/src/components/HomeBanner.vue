<template>
    <section id="hero">
        <h4>Échange équitable</h4>
        <h2>Offres super avantageuses</h2>
        <h1>Sur tous les Produits</h1>
        <p>Économisez plus avec <strong style="font-weight: 700;">MA.Chine</strong> et jusqu'à 20 % de réduction par rapport aux prix habituels !</p>
        <button>
          <RouterLink to="/product/all">Achetez Maintenant</RouterLink>
        </button>
    
    </section>

    <div class="header_line_title">
      <h3>Produits Qui Pourraient Vous Plaire</h3>
    </div>

</template>


<style>
h1{
  font-size: 50px;
  color: #222;
}
 
h2{
  font-size: 46px;
  line-height: 54px;
  color: #222;
}

h4{
  font-size: 18px;
  color: #222;
}


p{
  font-size: 16px;
  color: #465b52;
  margin: 15px 0 20px 0
}

#hero{
  margin: -68px -22% 0 -22%;
  background-image: url(@/assets/hero.png);
  height: 50vh;
  background-size: cover;
  background-position: top 25% right 0;
  padding: 80px 15% 0 15%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  line-height: 1;
  overflow-x: hidden;
}

#hero h1{
  color: #088178;
  
}

#hero h4{
  padding-bottom: 15px;
 
}

#hero button {
  background-image: url(@/assets/button.png);
  background-color: transparent;
  color: #088178;
  border: 0;
  padding: 14px 60px 18px 65px;
}

#hero button a {
  color: #088178;
  padding-top: 10px;
  padding-bottom: 10px;
}

.header_line_title {
    margin-top: 10px;
    margin-bottom: 20px;
    border-bottom: 3px solid #088178;
    width: 160px;
    white-space: nowrap;
    overflow: visible;
}

@media (max-width: 920px) {

h1{
  font-size: 36px;
  color: #222;
}

h2{
  font-size: 28px;
  line-height: 32px;
  margin-bottom: 5px;
  color: #222;
}

#hero{
  margin: -68px -14% 0 -14%;
  padding: 20px 15% 0 15%;
  background-position: top 30% right 30%
 }
  
}

@media (max-width: 477px) {
 
  #hero{
    margin: -64px -6% 0 -6%;
    padding: 48px 5% 0 5%;
    background-position: 74%;
  }
  
  h2 {
    font-size: 28px
  }
  
  h1{
    font-size: 24px
  }
  
  p{
    line-height: 20px;
    font-size: 12px;
  }
  
  #hero button{
    margin-right: 10px
  }
  
}

</style>