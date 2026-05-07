const fileInput = document.getElementById(
    "fileInput"
);

const previewContainer = document.getElementById(
    "previewContainer"
);

const imageCount = document.getElementById(
    "imageCount"
);

const uploadForm = document.getElementById(
    "uploadForm"
);

const loadingBox = document.getElementById(
    "loadingBox"
);

const successBox = document.getElementById(
    "successBox"
);

const generateBtn = document.getElementById(
    "generateBtn"
);


fileInput.addEventListener(
    "change",
    function () {

        previewContainer.innerHTML = "";

        successBox.classList.add(
            "hidden"
        );

        const files = this.files;

        imageCount.innerText = files.length;


        // NO LIMIT NOW
        for (let file of files) {

            const reader = new FileReader();

            reader.onload = function (e) {

                const card = document.createElement(
                    "div"
                );

                card.classList.add(
                    "preview-card"
                );

                card.innerHTML = `
                    <img src="${e.target.result}">
                    
                    <div class="preview-name">
                        ${file.name}
                    </div>
                `;

                previewContainer.appendChild(
                    card
                );
            };

            reader.readAsDataURL(file);
        }

    }
);



uploadForm.addEventListener(
    "submit",
    function (event) {

        const files = fileInput.files;


        // REQUIRE AT LEAST 1 IMAGE
        if (files.length < 1) {

            event.preventDefault();

            alert(
                "Please upload at least 1 image"
            );

            return;
        }


     
        successBox.classList.add(
            "hidden"
        );


    
        loadingBox.classList.remove(
            "hidden"
        );


        
        generateBtn.disabled = true;

        generateBtn.innerText =
            "Generating PDF...";


      
        setTimeout(() => {

            loadingBox.classList.add(
                "hidden"
            );

            successBox.classList.remove(
                "hidden"
            );

            generateBtn.disabled = false;

            generateBtn.innerText =
                "Generate A4 PDF";

        }, 5000);

    }
);