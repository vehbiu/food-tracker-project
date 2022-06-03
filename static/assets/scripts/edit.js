
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#add-ingredient").addEventListener("click", () => {

    /** @type {HTMLElement} */
    const ingredients = document.querySelector("#ingredient-list");

    const newDiv = document.createElement("div");
    newDiv.innerHTML = `
            <div class="input-group w-ing m-auto ing" autocomplete="off" id="ingredient-list">
                <input class="form-control btn-outline-secondary mw-5 ing" type="number" name="amount"
                    placeholder="Amount">
                <input type="text" class="form-control mw-20 ing" name="unit" placeholder="Unit">
                <input type="text" class="form-control ing" name="name" placeholder="Ingredient Name">
            </div>
        `;
    ingredients.appendChild(newDiv);
  });

  document.querySelector("#ch-btn").addEventListener("click", async (e) => {
    e.preventDefault();
    /** @type {HTMLFormElement} */
    const form = document.querySelector("#ch-form");
    const data = Object.fromEntries(new FormData(form));
    const response = await fetch(window.location.href.trimEnd("/") + "/general", {
      method: "POST",
      headers: { "Content-Type": "application/json", },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    if (json.status === "OK") {
      return Toast.success("Recipe updated successfully!");
    }
    Toast.error(json.msg);
  })

})

class Ingredient {
  /**
   * @param {string} name
   * @param {string} unit
   * @param {number} amount
   */
  constructor(name, unit, amount) {
    this.name = name;
    this.unit = unit;
    this.amount = amount;
  }

  getName() {
    return this.name;
  }

  getUnit() {
    return this.unit;
  }

  getAmount() {
    return this.amount;
  }
}

/**
 * 
 * @param {HTMLObjectElement} object;
 */
function deleteStep(object) {
  object.parentElement.parentElement.parentElement.remove();
}

function addStep() {
  const steps = document.querySelector(".step-container");
  const newDiv = document.createElement("div");
  newDiv.classList.add("step");
  newDiv.innerHTML = `
      <p class="step-number">?.</p>
      <!-- <input type="text" class="form-control step-text" placeholder="Step Content" value="{{ recipe.steps[i] }}"> -->
      <div class="input-group mb-3" data-step="{{ i + 1 }}">
        <input type="text" class="form-control" name="step-content" placeholder="Step Content" aria-label="Step Content"
          aria-describedby="step-actions">
        <span class="input-group-text" id="step-actions">
          <a href="#" onClick="deleteStep(this)"><i class="fa-solid fa-trash me-1" style="color: red"></i></a>
          <a href="#" onClick="addStep();" class="step-number"><i class="fa-solid fa-plus fs-5"></i></a>
        </span>
      </div>
    `;
  steps.appendChild(newDiv);
}

function parseSteps() {
  const steps = document.querySelectorAll(".step");
  const stepList = [];
  steps.forEach(step => {
    const stepData = step.querySelector("input");
    if (stepData === null) return;
    stepList.push(stepData.value);
  });
  return stepList;
}

function parseIngredients() {
  const ingredients = document.querySelectorAll("#ingredient-list");
  const ingredientList = [];
  ingredients.forEach(elem => {
    const amount = elem.querySelector("input[name=amount]").value;
    ingredientList.push({
      name: elem.querySelector("input[name=name]").value,
      unit: elem.querySelector("input[name=unit]").value,
      amount: amount === "" ? 0 : amount,
    });
  });
  return ingredientList;
}

async function submitRecipe() {
  const data = {
    steps: parseSteps(),
    ingredients: parseIngredients(),
  };
  const response = await fetch(window.location.href.trimEnd("/").replace("#", "") + "/data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const json = await response.json();
  if (json.status === "OK") {
    return Toast.success("Recipe updated successfully!");
  }
  Toast.error(json.msg);
}


document.querySelector("#submit-recipe").addEventListener("click", () => submitRecipe());