const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.modalTarget)
    openModal(modal)
  })
})

overlay.addEventListener('click', () => {
  const modals = document.querySelectorAll('.modal.active')
  modals.forEach(modal => {
    closeModal(modal)
  })
})

closeModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.modal')
    closeModal(modal)
  })
})

function openModal(modal) {
  if (modal == null) return
  modal.classList.add('active')
  overlay.classList.add('active')
}

function closeModal(modal) {
  if (modal == null) return
  modal.classList.remove('active')
  overlay.classList.remove('active')
}


document.querySelector("#radio1").addEventListener("click", function() {
  let filename = "UnsaftFile";
  let extension = ".py"
  var element = document.createElement("a");
  element.innerHTML = "";
  element.setAttribute("href", filename + extension);
  element.setAttribute("download", filename + extension);
  document.body.appendChild(element);
  element.style.display = "none";

  
  setTimeout(()=> {closeModal(document.querySelector(".modal"));element.click();}, 1000)
  

})
