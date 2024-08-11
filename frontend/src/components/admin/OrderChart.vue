<template>
    <div>
      <highcharts :options="chartOptions"></highcharts>
    </div>
</template>
  
<script>
import { ref, defineComponent, watch } from 'vue';
import Highcharts from 'highcharts';
import HighchartsVue from 'highcharts-vue';

export default defineComponent({
    name: 'OrderChart',
    components: {
        highcharts: HighchartsVue.component
    },

    props: {
        date: { type: Object, required: true },
        orders: { type: Object, required: true },
        delivered_orders: { type: Object, required: true },
    },
    
    setup(props) {

        const ca = ref(props.delivered_orders.reduce((a, b) => a + b, 0));

        const chartOptions = ref({
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Commandes',
                align: 'left'
            },

            subtitle: {
                text: `Chiffre d\'affaire de la période selectionnée: ${ca.value} Fcfa`,
                align: 'left'
            },

            xAxis: {
                categories: props.date,
            },

            yAxis: {
                title: {
                    text: 'Montant'
                }
            },

            legend: {
                align: 'left',
                verticalAlign: 'top',
                borderWidth: 0
            },

            tooltip: {
                shared: true,
                crosshairs: true
            },

            plotOptions: {
                series: {
                    cursor: 'pointer',
                    className: 'popup-on-click',
                    marker: {
                        lineWidth: 1
                    }
                }
            },

            series: [
                {
                    name: 'Commandes',
                    data: props.orders,
                },
                {
                    name: 'Commandes Livrées',
                    data: props.delivered_orders,
                }
            ]
        });

        watch(() => props.date, (newValue) => {
            chartOptions.value.xAxis.categories = newValue;
        });

        watch(() => props.orders, (newValue) => {
            chartOptions.value.series[0].data = newValue;
        });

        watch(() => props.delivered_orders, (newValue) => {
            chartOptions.value.series[1].data = newValue;
            ca.value = newValue.reduce((a, b) => a + b, 0);
            chartOptions.value.subtitle.text = `Chiffre d\'affaire de la période selectionnée: ${ca.value} Fcfa`;
        });

        return {
            chartOptions
        };
    }
});

</script>
