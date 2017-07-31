import { ClientDriverPage } from './app.po';

describe('client-driver App', function() {
  let page: ClientDriverPage;

  beforeEach(() => {
    page = new ClientDriverPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
