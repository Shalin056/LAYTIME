// C:\Users\shali\Documents\shalin\test-app\src\Laytime\Screens\DashBoard.js

import React, { Component } from 'react';
import * as echarts from 'echarts/core';
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import { PieChart } from 'echarts/charts';
import { LabelLayout } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import { getDashData } from '../../components/DataProvider';
import 'swfrontend/DASHBOARD/Dashboard.css';

echarts.use([TitleComponent, TooltipComponent, LegendComponent, PieChart, CanvasRenderer, LabelLayout]);

class MyResponsivePie extends Component {
    constructor(props) {
        super(props);
        this.chartRef = React.createRef();
        this.state = {
            data: [],
            isLoading: true,
            isDarkTheme: localStorage.getItem('theme') === 'dark',
        };
    }

    componentDidMount() {
        this.fetchDashData();
    }

    fetchDashData = () => {
        getDashData()
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    localStorage.setItem('is_requester', data[0].is_requester);
                }
                this.setState({ data: data, isLoading: false }, () => {
                    this.initChart();
                });
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                this.setState({ isLoading: false });
            });
    };

    initChart = () => {
        const { data, isDarkTheme } = this.state; 
        const chartDom = this.chartRef.current;
        if (!chartDom) {
            console.error('Invalid DOM element for chart initialization.');
            return;
        }
        const myChart = echarts.init(chartDom,);

        const theme = {
            color: [
                '#3366CC',
                '#33CCCC',
                '#FFD700',
                '#FF3333',
                '#CC3399',
                '#FF6600',
                '#87CEEB',
                '#98FB98',
                '#E6E6FA',
                '#FF7F50',
                '#EE82EE',
                '#FFDAB9',
            ],
        };

        const textColor = isDarkTheme ? 'white' : 'black'; 

        const option = {
            title: {
                text: 'Status of Records',
                left: 'center',
                top: 5,
                textStyle: {
                    fontSize: '15px',
                    color: textColor, 
                },
            },
            tooltip: {
                trigger: 'item',
            },
            legend: {
                orient: 'vertical',
                left: 20,
                top: 100,
                align: 'left',
                itemWidth: 20,
                itemHeight: 10,
                formatter: function (name) {
                    const item = data.find(item => item.name === name);
                    if (name === 'Approved' || name === 'Rejected') {
                        return `${name}: ${item.value}`;
                    } else {
                        return `Pending from ${name}: ${item.value}`;
                    }
                },
                textStyle: {
                    fontSize: 14,
                    fontWeight: 'bold',
                    color: textColor,
                },
            },
            series: [
                {
                    name: 'Access From',
                    type: 'pie',
                    radius: ['45%', '75%'],
                    avoidLabelOverlap: false,
                    padAngle: 2,
                    itemStyle: {
                        borderRadius: 5,
                    },
                    label: { fontSize: 14, color: textColor,},
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: 16,
                            fontWeight: 'bold',
                            color: textColor,
                        },
                    },
                    data: data,
                },
            ],
            ...theme,
        };
        myChart.setOption(option);

        // myChart.on('click', params => {
        //     const selectedName = params.name;
        //     console.log('selectedName: ', selectedName);
            
        //     let pathname;
        //     if (data[0].is_requester === false) {
        //         pathname = `${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeApprovals`;
        //     } else {
        //         pathname = `${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator`;
        //     }
        
        //     this.props.history.push({
        //         pathname: pathname,
        //         searchQuery: selectedName,
        //         is_requester: data[0].is_requester
        //     });
        // });
        
    };

    toggleTheme = () => {
        const { isDarkTheme } = this.state;
        const newTheme = isDarkTheme ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme); 
        this.setState({ isDarkTheme: !isDarkTheme }, () => {
            this.initChart();
        });
    };

    render() {
        const { isDarkTheme, isLoading, data } = this.state; 
        const buttonTitle = isDarkTheme ? 'Light' : 'Dark';
        const backgroundColor = isDarkTheme ? '#0f172a' : '#f3eded';
        const color = isDarkTheme ? 'white' : 'black'; 

        return (
            <div>
                {isLoading ? (
                    <p>Loading...</p>
                ) : data.length > 0 ? (
                    <><div><h1 className='h1Style' style={{fontSize:'20px'}}>DashBoard</h1></div>
                        <div style={{ backgroundColor: backgroundColor, transition: 'background-color 0.3s' }}>
                            <label className="switch" style={{ cursor: 'pointer' }}>
                                <input type="checkbox" checked={isDarkTheme} onChange={this.toggleTheme} style={{ display: 'none' }} />
                                <span className="slider round" style={{ backgroundColor: isDarkTheme ? '#2196F3' : '#ccc', borderRadius: '20px', width: '40px', height: '20px', position: 'relative', display: 'inline-block', margin: '10px 0px 0px 10px' }}>
                                    <span className="circle" style={{ backgroundColor: 'white', borderRadius: '50%', width: '16px', height: '16px', position: 'absolute', top: '2px', left: isDarkTheme ? '2px' : '22px', transition: 'left 0.3s ease-in-out' }}></span>
                                </span>
                            </label>
                        </div>
                        <div ref={this.chartRef} style={{ backgroundColor: backgroundColor, width: 'auto', height: '75vh', transition: 'background-color 0.3s'}}></div>
                    </>
                ) : (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh', flexDirection: 'column' }}>
                        <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'red', display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '20px' }}>
                            <div style={{ color: 'white', fontSize: '30px', lineHeight: 0 }}>
                                X
                            </div>
                        </div>
                        <p style={{ textAlign: 'center', color: 'black', fontSize: '1.5rem' }}>No Data Available</p>
                    </div>
                )}
            </div>
        );
    }
}

export default MyResponsivePie;