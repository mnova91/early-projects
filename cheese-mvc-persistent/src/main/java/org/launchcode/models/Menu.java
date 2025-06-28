package org.launchcode.models;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.ArrayList;
import java.util.List;

@Entity
public class Menu {

    //Class properties

    @Id
    @GeneratedValue
    private int id;

    @NotNull
    @Size(min=3, max=15)
    private String name;

    @ManyToMany
    private List<Cheese> cheeses = new ArrayList<>();

    //Getters and Setters

    public int getId() { return id; }

    public List<Cheese> getCheeses() { return cheeses; }

    public void addItem(Cheese item) { cheeses.add(item); }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    //Constructors

    public Menu() {  }
    public Menu(String name) { this.name = name; }



}


