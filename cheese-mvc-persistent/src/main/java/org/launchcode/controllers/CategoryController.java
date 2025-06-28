package org.launchcode.controllers;

import org.launchcode.models.Category;
import org.launchcode.models.data.CategoryDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.Errors;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.validation.Valid;

@Controller
@RequestMapping(value = "category")
public class CategoryController {

    @Autowired
    private CategoryDao categoryDao;

    @RequestMapping(value = "")
    public String index(Model templateVariables) {
        templateVariables.addAttribute("title", "All Categories");
        templateVariables.addAttribute("categories", categoryDao.findAll());
        return "category/index"; }

    @RequestMapping(value = "add")
    public String add(Model templateVariables) {
        templateVariables.addAttribute("title", "Add Category");
        templateVariables.addAttribute("category", new Category());
        return "category/add"; }

    @RequestMapping(value = "add", method = RequestMethod.POST)
    public String add(@ModelAttribute @Valid Category category,
                      Errors errors, Model model) {
        categoryDao.save(category);
        return "redirect:"; }

}
