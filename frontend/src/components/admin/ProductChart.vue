<template>
    <div>
      <highcharts :options="chartOptions"></highcharts>
    </div>
</template>
  
<script>
import { defineComponent, ref } from 'vue';
import Highcharts from 'highcharts';
import HighchartsVue from 'highcharts-vue';

export default defineComponent({
    name: 'ProductChart',
    components: {
        highcharts: HighchartsVue.component
    },
            
    props: {
        data: { type: Object, required: true },
    },

    setup(props) {

        const chartOptions = ref({
            chart: {
                zooming: {
                    type: 'xy'
                }
            },
            title: {
                text: 'Produits',
                align: 'left'
            },
            subtitle: {
                text: '12 Produits les plus commandés recemment (depuis un mois)',
                align: 'left'
            },
            xAxis: [{
                categories: props.data.value.categories,
                labels: {
                    enabled: false  // Hide x-axis labels
                },
                title: {
                    text: 'Produits'
                },
                crosshair: true
            }],
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Quantité',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }, { // Secondary yAxis
                title: {
                    text: 'Quantité',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: true
            },
            legend: {
                align: 'left',
                verticalAlign: 'top',
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || // theme
                    'rgba(255,255,255,0.25)'
            },
            series: [{
                name: 'Produits',
                type: 'column',
                yAxis: 1,
                data: props.data.value.products,

            }, {
                name: 'Panier d\'achat',
                type: 'spline',
                data: props.data.value.carts,
            }]
        });

        return {
            chartOptions
        };
    }
});

</script>
