/*
 * Factory.cpp
 *
 *  Created on: Jan 30, 2025
 *      Author: som
 */
#include "Factory.h"
Factory* Factory::instance = NULL;

Factory* Factory:: getInstance(){
        if(Factory::instance == NULL){
            Factory::instance = new Factory();
        }
        return Factory::instance;
    }

Food* Factory::makeFood(const string& type){
        if(type.compare("bi") == 0){
            return new Biscuit();
        }
        if(type.compare("ch") == 0){
            return new Chocolate();
        }

        return NULL;
    }
