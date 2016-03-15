export class GestaolivrePage {
  navigateTo() { return browser.get('/'); }
  getParagraphText() { return element(by.css('Gestaolivre-app p')).getText(); }
}
