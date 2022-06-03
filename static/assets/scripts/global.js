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

class Step {
  constructor(content) {
    this.content = content;
  }

  addStep() { };
}


class Recipe {
  /**
   * @param {list}
   */
  constructor(recipes, steps) {
    this.recipes = recipes;
    this.steps = steps;
  }
  /**
   * @returns {Array<Step>}
   */
  getSteps() {
    return this.steps;
  }

  addStep(step) {
    this.steps.addStep(step);
  }
}


class API {
  /**
   * @param {string} base
   */
  constructor(base) {
    this.base = base;
  }

  /**
   * @param {string} path
   * @param {string} method
   * @param {string} body
   * @returns {Promise<Response>}
   * @private
   * @memberof API
   */
  async _request(path, method, body) {
    const response = await fetch(this.base + path, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: body,
    });
    return response;
  }

}

