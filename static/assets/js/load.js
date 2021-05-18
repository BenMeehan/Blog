const loadmore = document.querySelector("#loadmore");
let currentItems = 3;
loadmore.addEventListener("click", (e) => {
  const elementList = [...document.querySelectorAll(".list .list-element")];
  for (let i = currentItems; i < currentItems + 3; i++) {
    if (elementList[i]) {
      elementList[i].style.display = "block";
    }
  }
  currentItems += 3;

  if (currentItems >= elementList.length) {
    e.target.style.display = "none";
  }
});
