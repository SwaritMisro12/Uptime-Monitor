//still under development

// function handleHover(ip) {
 //   fetch(`/last_outages?ip=${ip}`)
  //      .then(response => response.json())
 //       .then(data => {
 //           const outagesContainer = document.getElementById('lastOutages');
//            outagesContainer.innerHTML = '';  // Clear previous outages

   //         if (data.outages.length > 0) {
    //            const outagesList = document.createElement('ul');

    //            data.outages.forEach(outage => {
     //               const outageItem = document.createElement('li');
    //                outageItem.textContent = `Start Time: ${outage.start_time}, End Time: ${outage.end_time}, Duration: ${outage.duration}`;
     //               outagesList.appendChild(outageItem);
    //            });

    //            const tooltipContainer = document.createElement('div');
     //           tooltipContainer.classList.add('tooltip');
     //           tooltipContainer.appendChild(outagesList);

     //           const tooltipContent = document.createElement('div');
     //           tooltipContent.classList.add('tooltip-content');
     //           tooltipContent.appendChild(tooltipContainer);

     //           outagesContainer.appendChild(tooltipContent);
      //      } else {
     //           outagesContainer.textContent = 'No outages recorded.';
    //        }
     //   });
//}
