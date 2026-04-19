/*
 * Factory.h
 *
 *  Created on: Mar 10, 2021
 *      Author: som
 */

#ifndef FACTORY_H_
#define FACTORY_H_

#include <nanobind/nanobind.h>
#include <iostream>
#include <string>

#include "Biscuit.h"
#include "Chocolate.h"

using namespace std;

class Factory{
public:
    static Factory* instance;
    static Factory* getInstance();

    Food* makeFood(const string& type);

private:
    Factory(){}

    // Delete copy constructor & assignment operator (Singleton pattern)
    Factory(const Factory&) = delete;
    Factory& operator=(const Factory&) = delete;
};
//Factory* Factory:: instance =  NULL;


#endif /* FACTORY_H_ */
