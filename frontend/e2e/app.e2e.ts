/// <reference path="../typings/main.d.ts" />

import { GestaolivrePage } from './app.po';

describe('gestaolivre App', function() {
  let page: GestaolivrePage;

  beforeEach(() => {
    page = new GestaolivrePage();
  })

  it('should display message saying app works', () => {
    page.navigateTo()
    expect(page.getParagraphText()).toEqual('gestaolivre Works!');
  });
});
