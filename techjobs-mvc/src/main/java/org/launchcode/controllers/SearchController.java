package org.launchcode.controllers;

import org.launchcode.models.JobData;
import org.springframework.boot.autoconfigure.batch.BatchProperties;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by LaunchCode
 */
@Controller
@RequestMapping("search")
public class SearchController {

    @RequestMapping(value = "")
    public String search(Model model) {
        model.addAttribute("columns", ListController.columnChoices);
        return "search";
    }
    // TODO #1 - Create handler to process search request and display results

    @RequestMapping(value ="results")
    public String results(Model model, @RequestParam String searchType, @RequestParam String searchTerm) {
        String title = "TechJobs";

        if (searchType.toLowerCase().equals("all") && searchTerm.equals("")) {
            ArrayList<HashMap<String,String>> jobs = JobData.findAll();
            model.addAttribute("columns", ListController.columnChoices);
            model.addAttribute("jobs", jobs);
            model.addAttribute("title", title);
            return "list-jobs";
        }

        else if (searchType.toLowerCase().equals("all")) {
            ArrayList<HashMap<String,String>> jobs = JobData.findByValue(searchTerm);
            model.addAttribute("columns", ListController.columnChoices);
            model.addAttribute("jobs", jobs);
            model.addAttribute("title", title);
            return "search";
        }

        else {
            ArrayList<HashMap<String,String>> jobs = JobData.findByColumnAndValue(searchType, searchTerm);
            model.addAttribute("columns", ListController.columnChoices);
            model.addAttribute("jobs", jobs);
            model.addAttribute("title", title);
            return "search";
        }
    }
}
