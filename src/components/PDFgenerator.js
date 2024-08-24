// C:\Users\shali\Documents\shalin\test-app\src\components\PDFgenerator.js

import jsPDF from 'jspdf'; 
import "jspdf-autotable";
import { getPdfData} from '../components/DataProvider';

export const downloadPDF = async(id) => {
    
        try {
            if (!id) {
                throw new Error('No row selected or more than one row selected.');
            }

            const response = await getPdfData(id);
            console.log('=================')
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const rowData = await response.json();
            
            const doc = new jsPDF();
     
            const shippingDetail = rowData.ship_detail;
            console.log(shippingDetail)
            delete shippingDetail.remarks
            const stages = rowData.stages;
            const split_quantities = rowData.split_quantities;
            const laytime_calculator = rowData.laytime_calculator;
            // const total_laytime_timediff = rowData.total_time_difference;
            
            const shipDetailEntries = Object.entries(shippingDetail);
            const halfLength = Math.ceil(shipDetailEntries.length / 2);
            const firstHalf = shipDetailEntries.slice(0, halfLength);
            const secondHalf = shipDetailEntries.slice(halfLength);

            const calculationEntries = Object.entries(laytime_calculator);
            const calHalfLength = Math.ceil(calculationEntries.length / 2);
            const calFirstHalf = calculationEntries.slice(0, calHalfLength);
            const calSecondHalf = calculationEntries.slice(calHalfLength);

            const formatTime = (seconds) => {
                const hours = Math.floor(seconds / 3600);
                const minutes = Math.floor((seconds % 3600) / 60);
                const remainingSeconds = seconds % 60;
                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
            };
            
            const sumTimeDifference = stages.reduce((total, stage) => {
                
                const timeDiff = stage['time_difference_(HH:MM:SS)'] || '00:00:00';
                console.log('count: ',stage)
                const [hours, minutes, seconds] = timeDiff.split(':').map(Number);
                total += hours * 3600 + minutes * 60 + seconds;
                return total;
            }, 0);

            const totalRow = {
                'START DATE TIME': '',
                'END DATE TIME': '',
                'STAGE NAME': '',
                'PERCENTAGE': '',
                'IS INCLUDED': '',
                'TIME DIFFERENCE (HH:MM:SS)': { content: formatTime(sumTimeDifference), styles: { fontStyle: 'bold' } },
                'TOTAL LAYTIME USED (DAYS)': ''
            };
    
            stages.push(totalRow);

            const addTable = (title, data, startY, styles = {}, margin = {}) => {
                const tableBlock = () => {
                    const italicFontStyle = 'italic';
                    doc.setFont(undefined, italicFontStyle);
                    doc.text(title, 15, startY);
            
                    const formattedData = data.map(([key, value]) => {
                        return [key.replace(/_/g, " ").toUpperCase(), value];
                    });

                    const headerStyles = {
                        fillColor: [219, 64, 64],
                        textColor: [255, 255, 255],
                    };
            
                    if (title === "Calculation:") {
                        const tableHeight = formattedData.length * 10 + 15;
                        const remainingSpace = 290 - startY;
                        if (tableHeight > remainingSpace) {
                            doc.addPage();
                            startY = 30;
                        }
                    }
            
                    doc.autoTable({
                        body: formattedData,
                        startY: startY + 6,
                        theme: 'striped',
                        tableWidth: 70,
                        styles: styles,
                        margin: margin,
                        didDrawCell: (data) => {
                            if (data.section === 'head') {
                                data.cell.styles = { fillColor: [219, 64, 64], textColor: [255, 255, 255], halign: 'center', cellWidth: 50, };
                            }
                        },
                        headStyles: {
                            fillColor: headerStyles.fillColor,
                            textColor: headerStyles.textColor,
                            fontStyle: 'bold',
                        },
                        columnStyles: {
                            0: {
                                halign: 'left',
                                cellWidth: 40,
                                fontStyle: 'bold',
                                textColor: [0, 0, 0],
                            },
                            1: {
                                cellWidth: 40,
                                textColor: [0, 0, 0],
                            },
                        }
                    });
            
                    return doc.lastAutoTable.finalY + 10;
                };
            
                // Check if table is near the bottom of the page and move to next page if needed
                const tableHeight = startY + 5 + data.length * 10;
                if (tableHeight > 260) {
                    doc.addPage();
                    startY = 30;
                }
            
                startY = tableBlock();
            
                return startY;
            };

            const addTable2 = (title, data, startY) => {
                const headerStyles = {
                    fillColor: [219, 64, 64],
                    textColor: [255, 255, 255],
                };
            
                const tableBlock = () => {
                    doc.text(title, 15, startY);
            
                    const dataList = [];
                    const keysList = [];
                    const valuesList = [];
            
                    if (Array.isArray(data) && data.length > 0 && typeof data[0] === 'object') {
                        data.forEach((item, index) => {
                            const subValues = {};
            
                            Object.entries(item).forEach(([fieldName, value]) => {
                                subValues[fieldName] = value;
                            });
            
                            dataList.push(subValues);
                        });
            
                        const subValuesList = [];
                        dataList.forEach(item => {
                            const newItem = { ...item[1] };
            
                            subValuesList.push(newItem);
                        });
            
                        const keys = Object.keys(subValuesList[0]).map(each => each.replace(/_/g, " ").toUpperCase());
                        keysList.push(keys);
            
                        subValuesList.forEach(obj => {
                            const formattedValues = Object.values(obj).map(value => {
            
                                if (typeof value === 'boolean') {
                                    return value ? 'Yes' : 'No';
                                } else {
                                    return value;
                                }
                            });
            
                            valuesList.push(formattedValues);
                        });
            
                        if (title === "Split Quantities:"){
                            let tableHeight = valuesList.length * 10 + 15;
                            let remainingSpace = 290 - startY;
                            if (tableHeight > remainingSpace) {
                                doc.addPage();
                                startY = 30;
                            }
                        }
            
                        doc.autoTable({
                            head: keysList,
                            body: valuesList,
                            theme: 'grid',
                            startY: startY + 6,
                            styles: { fontSize: 8, halign: 'center', textColor: [0, 0, 0],},
                            didDrawCell: (data) => {
                                if (data.section === 'head') {
                                    data.cell.styles = { fillColor: [219, 64, 64], textColor: [255, 255, 255], fontStyle: 'bold', halign: 'center', cellWidth: 20 };
                                }
                            },
                            headStyles: {
                                fillColor: headerStyles.fillColor,
                                textColor: headerStyles.textColor,
                                fontStyle: 'bold',
                            },
                        });
            
                        startY = doc.lastAutoTable.finalY + 10;
            
                    }
            
                    return startY;
                };

                if (title === "Split Quantities:"){
                    const tableHeight = doc.autoTable.previous.finalY + 10 + data.length * 10;
                    if (tableHeight > 260) {
                        doc.addPage();
                        startY = 30;
                    }
                }

                startY = tableBlock();
            
                return startY;
            };
            
            // Add shipping details table
            let currentY = 30;

            let ship = addTable("Ship Detail:", firstHalf, currentY, { fontSize: 8, fillColor: [255, 255, 255] }, { left: 15, top: 100 });

            // Add second half of Ship Detail fields table
            currentY = addTable("", secondHalf, 30, { fontSize: 8, fillColor: [255, 255, 255] }, { left: 115, top: 0 });
            // currentY += 5;

            currentY = addTable("Calculation:", calFirstHalf, ship+1, { fontSize: 8, fillColor: [255, 255, 255] }, { left: 15, top: 100 });
            
            // currentY = addTable("", calSecondHalf, 110 , { fontSize: 8, fillColor: [255, 255, 255] }, { left: 115, top:0  });
            currentY = addTable("", calSecondHalf, ship+1 , { fontSize: 8, fillColor: [255, 255, 255] }, { left: 115, top:0  });

            if (split_quantities && split_quantities.length > 0) {
                currentY = addTable2("Split Quantities:", Object.entries(split_quantities), currentY + 0.5);
                console.log('currentY after SPLIT: ', currentY)
                currentY = addTable2("Shipping Stages:", Object.entries(stages), currentY );
                console.log('currentY after STAGE: ', currentY)
            }
            else{
                currentY = addTable2("Shipping Stages:", Object.entries(stages), currentY + 5);
                console.log('currentY after STAGE: ', currentY)
            }
            
            // currentY = addTable("", Object.entries(total_laytime_timediff), currentY + 5);
            
            // Add shipping stages table
            // currentY = addTable2("Shipping Stages:", Object.entries(stages), 130);

            // Add split quantities table
            // if (split_quantities && split_quantities.length > 0) {
            //     currentY = addTable2("Split Quantities:", Object.entries(split_quantities), currentY + 5);
            // }

            // Add calculation details table
            // currentY = addTable("Calculation:", Object.entries(laytime_calculator), currentY + 1, { fontSize: 8, fillColor: [255, 255, 255] });

            // Add page numbers in footer

            const currentDate = new Date();
            const formattedDate = `${currentDate.toLocaleDateString()} ${currentDate.toLocaleTimeString()}`;
            const totalPages = doc.internal.getNumberOfPages();
            for (let i = 1; i <= totalPages; i++) {
                doc.setPage(i);
                doc.setFontSize(8);
                doc.setTextColor(0,0,0);
                doc.setFont('helvetica', 'italic');  
                doc.text(200, 290, `Page ${i} of ${totalPages}`, { align: 'right' });
                // const currentDate = new Date();
                // const formattedDate = `${currentDate.toLocaleDateString()} ${currentDate.toLocaleTimeString()}`;
                doc.text(10, 290, `System Generated PDF on ${formattedDate}`, { align: 'left' });

                doc.setFont('helvetica', 'bolditalic'); 
                doc.setFontSize(16); 
                doc.setTextColor(219, 64, 64); 
                doc.text(200, 12, 'Laytime Calculations', { align: 'right' });
                // doc.addImage("/LAYTIME/AMNS_INDIA_LOGO.jpg", 'JPG', 5, 2, 25, 15, undefined, 'FAST');
                doc.addImage("/AMNS_INDIA_LOGO.jpg", 'JPG', 5, 2, 25, 15, undefined, 'FAST');
                const images = doc.internal.collections?.images;
                if (!images) {
                    console.log(`Image is not loaded on page ${i}`);
                }
            }

            // Add border around entire page
            const addPageBorder = (lineWidth, borderColor) => {
                const totalPages = doc.internal.getNumberOfPages();
                for (let i = 1; i <= totalPages; i++) {
                    doc.setPage(i);
                    doc.setLineWidth(lineWidth);
                    doc.setDrawColor(borderColor[0], borderColor[0], borderColor[0]);
                    doc.rect(5, 20, 200, 263);
                }
            };

            addPageBorder(0, [0, 0, 0]);

            doc.save(`${id}_laytime_calculation_${formattedDate}.pdf`);
        }catch(error) {
            console.error('Error fetching rowData:', error);
        };
};
