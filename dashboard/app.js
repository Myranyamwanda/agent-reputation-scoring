const tabButtons = document.querySelectorAll('.tab-button');
const forms = document.querySelectorAll('.auth-form');

for (const button of tabButtons) {
  button.addEventListener('click', () => {
    const target = button.dataset.target;

    tabButtons.forEach((tab) => tab.classList.toggle('active', tab === button));

    forms.forEach((form) => {
      form.classList.toggle('active', form.id === `${target}Form`);
    });
  });
}
