package org.launchcode.models.forms;

import org.launchcode.models.Cheese;
import org.launchcode.models.Menu;

import javax.validation.constraints.NotNull;

public class AddMenuItem {
    //variables

    private Menu menu;

    private Iterable<Cheese> cheeses;

    @NotNull private int menuId;

    @NotNull private int cheeseId;

    //getters and setters

    public Menu getMenu() { return menu; }

    public Iterable<Cheese> getCheeses() { return cheeses; }

    public int getMenuId() { return menuId; }
    public void setMenuId(int menuId) { this.menuId = menuId; }

    public void setMenu(Menu menu) { this.menu = menu; }

    public int getCheeseId() { return cheeseId; }
    public void setCheeseId(int cheeseId) { this.cheeseId = cheeseId; }

    //constructors

    public AddMenuItem() { }

    public AddMenuItem(Menu menu, Iterable<Cheese> cheeses) { this.menu = menu; this.cheeses = cheeses; }
}



