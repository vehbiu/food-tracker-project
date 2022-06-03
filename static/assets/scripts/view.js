
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
