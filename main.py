from chempy import Reaction, Substance
from dataclasses import dataclass
from drafter import *
from bakery import assert_equal

set_website_title("Chemistry Helper")
set_site_information(
    author="Arya Anilkumar",
    description="""A website that calculates limiting reactants,
    theoretical/percent yields, and interprets enthalpy values from a given reaction""",
    sources="Thanks to the TAs, Profs, and my friends",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/aryaanil-23/chemistry_help_final_project.git"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Compound:
    formula: str
    mass_g: float
    molar_mass: float
    coeff: int
    enthalpy: float

@dataclass
class State:
    reactants: dict[str, Compound]
    products: dict[str, Compound]
    desired_product: str
    limiting_reactant: str
    theoretical_yield: float
    enthalpy_rxn: float
    current_reactant: int
    current_product: int
    
initial_state = State({}, {}, "", "", 0.0, 0.0, 0, 0)

#route function unit tests came from drafter, sorry they are so long :(
@route
def index(state: State) -> Page:
    """
    Creates the home page where the user can input the
    reaction.
    
    Arg:
        state(State): the current state of the program
        
    Returns:
        Page: a page with the text box for the reaction and a button to
        route to the parse_reaction.
    """
    return Page(state, [
        "Enter a balanced reaction:\n",
        Text("please enter coefficients a space off the molecule: example: 2 H2 + O2 -> 2 H2O", style_color="crimson"),
        "\n",
        TextBox("reaction"),
        Button("Continue", "format_reaction")
               
        ])

assert_equal(index(State(reactants={}, products={}, desired_product='', limiting_reactant='', theoretical_yield=0.0, enthalpy_rxn=0.0, current_reactant=0, current_product=0)),
    Page(State(reactants={},
          products={},
          desired_product='',
          limiting_reactant='',
          theoretical_yield=0.0,
          enthalpy_rxn=0.0,
          current_reactant=0,
          current_product=0), [
        'Enter a balanced reaction:\n',
        Text('please enter coefficients a space off the molecule: example: 2 H2 + O2 -> 2 H2O', style_color='crimson'),
        '\n',
        TextBox('reaction'),
        Button('Continue', 'format_reaction'),
    ]))

def build_reaction(reaction_text: str) -> Reaction:
    """
    Takes the reaction input a string of the reaction and converts it into a Reaction dataclass
    with attributes reac: dict[str, int] and prod: dict[str, int] where the str is the
    formula of the compound and the int is the molar coefficient it has in the reaction.
    
    Utilizes from_string method defined in chempy, that parses string text based
    off of arrow (->) between product and reactants, and then splits the induvidual
    compound into their corresponding dicts.
    
    Needs a reaction input of at least 1 reactant -> at least 1 product, with the molar
    coefficients separated from the compound.
    ex) 2 H2 + O2 -> 2 H2O
    
    Args:
        reaction_text: str of the reaction from the user input TextBox in index
    Returns:
        Reaction: dataclass imported from chempy that has the attributes
            reac: dict[str, int]
            prod: dict[str, int]
        where str is the formula of the compound and int is the molar coefficient
        from the reaction.
    """
    return Reaction.from_string(reaction_text)
assert_equal(build_reaction("2 H2 + O2 -> 2 H2O"),
             Reaction({"H2": 2, "O2": 1}, {"H2O": 2}))
assert_equal(build_reaction("NaOH + HCl -> NaCl + H2O"),
             Reaction({"NaOH": 1, "HCl": 1}, {"NaCl": 1, "H2O": 1}))
assert_equal(build_reaction("H2 -> 2 H"),
             Reaction({"H2": 1},{"H": 2}))

@route
def format_reaction(state: State, reaction: str) -> Page:
    """
    Formats the given Reaction dataclass into dictionaries of Reactants
    and Products that update the current state.
    
    Args:
        state: the current State of the reaction
        reaction: the user inputted reaction string from the TextBox on index page.
    Returns:
        Page: returns the reactant_page with the updated state.
    """
    if not reaction:
        return Page(state, [
            "Error: No Reaction found!\n",
            Button("Back", "index")
            ])
    
    formatted_rxn = build_reaction(reaction)
    for reactant_formula, coeff in formatted_rxn.reac.items():
        state.reactants[reactant_formula] = Compound(
            reactant_formula, 0.0, Substance.from_formula(reactant_formula).mass,
            int(coeff), 0.0
            )
    for product_formula, coeff in formatted_rxn.prod.items():
        state.products[product_formula] = Compound(
            product_formula, 0.0, Substance.from_formula(product_formula).mass,
            int(coeff), 0.0
                )
    return reactant_page(state)

@route
def reactant_page(state: State) -> Page:
    """
    Creates a page that allows the user to input the mass and enthalpy value
    for a specific reactant.
    
    Args:
        state: current state of the program
    Returns:
        Page: page with the TextBox inputs for mass and enthalpy values and buttons
        to proceed or go back.
    """
    reactant_name = list(state.reactants.keys())[state.current_reactant]
    return Page(state, [
        f"Reactant: {reactant_name} \n",
        
        "Mass(g):",
        TextBox("mass"),
        
        "\nEnthalpy(kJ/mol):",
        TextBox("enthalpy"),"\n",
        
        Button("Next", "save_reactant"),
        Button("Back", "index")
        
        ])

assert_equal(format_reaction(
    State(reactants={}, products={}, desired_product='', limiting_reactant='', theoretical_yield=0.0, enthalpy_rxn=0.0, current_reactant=0, current_product=0),
    'HCl + NaOH -> NaCl + H2O'),
    Page(State(reactants={'HCl': Compound(formula='HCl',
                                     mass_g=0.0,
                                     molar_mass=36.458000000000006,
                                     coeff=1,
                                     enthalpy=0.0),
                     'NaOH': Compound(formula='NaOH',
                                      mass_g=0.0,
                                      molar_mass=39.99676928,
                                      coeff=1,
                                      enthalpy=0.0)},
          products={'H2O': Compound(formula='H2O',
                                    mass_g=0.0,
                                    molar_mass=18.015,
                                    coeff=1,
                                    enthalpy=0.0),
                    'NaCl': Compound(formula='NaCl',
                                     mass_g=0.0,
                                     molar_mass=58.43976928000001,
                                     coeff=1,
                                     enthalpy=0.0)},
          desired_product='',
          limiting_reactant='',
          theoretical_yield=0.0,
          enthalpy_rxn=0.0,
          current_reactant=0,
          current_product=0), [
        'Reactant: HCl \n',
        'Mass(g):',
        TextBox('mass'),
        '\nEnthalpy(kJ/mol):',
        TextBox('enthalpy'),
        '\n',
        Button('Next', 'save_reactant'),
        Button('Back', 'index'),
    ]))

@route
def save_reactant(state: State, mass: str, enthalpy: str) -> Page:
    """
    Saves the reactant information that was submitted. Each reactant's information
    is saved induvidually from each reactant's specific page submission.
    
    Args:
        state: current state of the program
        mass: mass string value inputted in the TextBox from reactant_page
        enthalpy: enthalpy string value inputted in the TextBox from reactant_page
    Returns:
        If there are no more reactants to input information for the program moves on
        to the select_desired_product page.
        Otherwise, it goes back to the reactant_page to input the next reactant's
        information.
    """
    reactant_name = list(state.reactants.keys())[state.current_reactant]
    state.reactants[reactant_name].mass_g = float(mass)
    state.reactants[reactant_name].enthalpy = float(enthalpy)
    state.current_reactant += 1
    if state.current_reactant >= len(state.reactants.keys()):
        return select_desired_product(state)
    return reactant_page(state)
assert_equal(save_reactant(State(reactants={'HCl': Compound(formula='HCl', mass_g=0.0, molar_mass=36.458000000000006, coeff=1, enthalpy=0.0), 'NaOH': Compound(formula='NaOH', mass_g=0.0, molar_mass=39.99676928, coeff=1, enthalpy=0.0)}, products={'H2O': Compound(formula='H2O', mass_g=0.0, molar_mass=18.015, coeff=1, enthalpy=0.0), 'NaCl': Compound(formula='NaCl', mass_g=0.0, molar_mass=58.43976928000001, coeff=1, enthalpy=0.0)}, desired_product='', limiting_reactant='', theoretical_yield=0.0, enthalpy_rxn=0.0, current_reactant=0, current_product=0), '3', '-92.3'),
    Page(State(reactants={'HCl': Compound(formula='HCl',
                                     mass_g=3.0,
                                     molar_mass=36.458000000000006,
                                     coeff=1,
                                     enthalpy=-92.3),
                     'NaOH': Compound(formula='NaOH',
                                      mass_g=0.0,
                                      molar_mass=39.99676928,
                                      coeff=1,
                                      enthalpy=0.0)},
          products={'H2O': Compound(formula='H2O',
                                    mass_g=0.0,
                                    molar_mass=18.015,
                                    coeff=1,
                                    enthalpy=0.0),
                    'NaCl': Compound(formula='NaCl',
                                     mass_g=0.0,
                                     molar_mass=58.43976928000001,
                                     coeff=1,
                                     enthalpy=0.0)},
          desired_product='',
          limiting_reactant='',
          theoretical_yield=0.0,
          enthalpy_rxn=0.0,
          current_reactant=1,
          current_product=0), [
        'Reactant: NaOH \n',
        'Mass(g):',
        TextBox('mass'),
        '\nEnthalpy(kJ/mol):',
        TextBox('enthalpy'),
        '\n',
        Button('Next', 'save_reactant'),
        Button('Back', 'index'),
    ]))

@route
def select_desired_product(state: State) -> Page:
    """
    A page where the user can select the desired product that they
    want to measure the yield of.
    
    Args:
        state: the current state of the reaction
    Returns:
        Page: a Page that allows the selection and then a button that links
        to the product_page
    """
    return Page(state, [
        "Select the desired product:",
        SelectBox("desired_product", list(state.products.keys())),
        
        Button("Next", "product_page")
        ])

@route
def product_page(state: State, desired_product: str) -> Page:
    """
    Creates a page that allows the user to input the mass and enthalpy value
    for a specific reactant. It also saves the desired product formula to the
    state. 
    
    Args:
        state: current state of the program
    Returns:
        Page: page with the TextBox inputs for actual yield and enthalpy values and buttons
        to proceed or go back.
    """
    state.desired_product = desired_product
    product_name = list(state.products.keys())[state.current_product]
    return Page(state, [
        
        f"Product: {product_name}\n",
        
        "Actual Yield(g) \n(input 0.0 if this product is not the Desired Product):\n",
        TextBox("actual_yield"),
        
        "\nEnthalpy(kJ/mol):",
        TextBox("enthalpy"), "\n",
        
        Button("Next", "save_product"),
        Button("Back", "reactant_page")
        ])

assert_equal(product_page(State(reactants={'HCl': Compound(formula='HCl', mass_g=3.0, molar_mass=36.458000000000006, coeff=1, enthalpy=-92.3), 'NaOH': Compound(formula='NaOH', mass_g=3.0, molar_mass=39.99676928, coeff=1, enthalpy=-416.88)}, products={'H2O': Compound(formula='H2O', mass_g=0.0, molar_mass=18.015, coeff=1, enthalpy=0.0), 'NaCl': Compound(formula='NaCl', mass_g=0.0, molar_mass=58.43976928000001, coeff=1, enthalpy=0.0)}, desired_product='', limiting_reactant='', theoretical_yield=0.0, enthalpy_rxn=0.0, current_reactant=2, current_product=0), 'NaCl'),
    Page(State(reactants={'HCl': Compound(formula='HCl',
                                     mass_g=3.0,
                                     molar_mass=36.458000000000006,
                                     coeff=1,
                                     enthalpy=-92.3),
                     'NaOH': Compound(formula='NaOH',
                                      mass_g=3.0,
                                      molar_mass=39.99676928,
                                      coeff=1,
                                      enthalpy=-416.88)},
          products={'H2O': Compound(formula='H2O',
                                    mass_g=0.0,
                                    molar_mass=18.015,
                                    coeff=1,
                                    enthalpy=0.0),
                    'NaCl': Compound(formula='NaCl',
                                     mass_g=0.0,
                                     molar_mass=58.43976928000001,
                                     coeff=1,
                                     enthalpy=0.0)},
          desired_product='NaCl',
          limiting_reactant='',
          theoretical_yield=0.0,
          enthalpy_rxn=0.0,
          current_reactant=2,
          current_product=0), [
        'Product: H2O\n',
        'Actual Yield(g) \n(input 0.0 if this product is not the Desired Product):\n',
        TextBox('actual_yield'),
        '\nEnthalpy(kJ/mol):',
        TextBox('enthalpy'),
        '\n',
        Button('Next', 'save_product'),
        Button('Back', 'reactant_page'),
    ]))

@route
def save_product(state: State, actual_yield: str, enthalpy: str) -> Page:
    """
    Saves the product information that was submitted. Each product's information
    is saved induvidually from each product's specific page submission.
    
    Args:
        state: current state of the program
        actual_yield: actual yield string value inputted in the TextBox from product_page
        enthalpy: enthalpy string value inputted in the TextBox from product_page
    Returns:
        If there are no more products to input information for the program moves on
        to the theoretical_yield_page.
        Otherwise, it goes back to the product_page to input the next product's
        information.
    """
    product_name = list(state.products.keys())[state.current_product]
    state.products[product_name].mass_g = float(actual_yield)
    state.products[product_name].enthalpy = float(enthalpy)
    state.current_product += 1
    if state.current_product >= len(state.products.keys()):
        return theoretical_yield_page(state)
    return product_page(state, state.desired_product)

assert_equal(save_product(State(reactants={'HCl': Compound(formula='HCl', mass_g=3.0, molar_mass=36.458000000000006, coeff=1, enthalpy=-92.3), 'NaOH': Compound(formula='NaOH', mass_g=3.0, molar_mass=39.99676928, coeff=1, enthalpy=-416.88)}, products={'H2O': Compound(formula='H2O', mass_g=0.0, molar_mass=18.015, coeff=1, enthalpy=0.0), 'NaCl': Compound(formula='NaCl', mass_g=0.0, molar_mass=58.43976928000001, coeff=1, enthalpy=0.0)}, desired_product='NaCl', limiting_reactant='', theoretical_yield=0.0, enthalpy_rxn=0.0, current_reactant=2, current_product=0), '0.0', '-293'),
    Page(State(reactants={'HCl': Compound(formula='HCl',
                                     mass_g=3.0,
                                     molar_mass=36.458000000000006,
                                     coeff=1,
                                     enthalpy=-92.3),
                     'NaOH': Compound(formula='NaOH',
                                      mass_g=3.0,
                                      molar_mass=39.99676928,
                                      coeff=1,
                                      enthalpy=-416.88)},
          products={'H2O': Compound(formula='H2O',
                                    mass_g=0.0,
                                    molar_mass=18.015,
                                    coeff=1,
                                    enthalpy=-293.0),
                    'NaCl': Compound(formula='NaCl',
                                     mass_g=0.0,
                                     molar_mass=58.43976928000001,
                                     coeff=1,
                                     enthalpy=0.0)},
          desired_product='NaCl',
          limiting_reactant='',
          theoretical_yield=0.0,
          enthalpy_rxn=0.0,
          current_reactant=2,
          current_product=1), [
        'Product: NaCl\n',
        'Actual Yield(g) \n(input 0.0 if this product is not the Desired Product):\n',
        TextBox('actual_yield'),
        '\nEnthalpy(kJ/mol):',
        TextBox('enthalpy'),
        '\n',
        Button('Next', 'save_product'),
        Button('Back', 'reactant_page'),
    ]))
    
@route
def theoretical_yield_page(state: State) -> Page:
    """
    Shows the theoretical yield, limiting reactant, and percent yield information
    from the given state.
    
    Args:
        state: the current state of the program
    Returns:
        Page: a page stating the limiting reactant, theoretical yield, and percent
        yield and a buttons to proceed to enthalpy_page or back.
            If no reactants are found, it produces an error message and provides a
            button to return back to index page.
    """
    if not state.reactants:
        return Page(state, [
            "No reactants found to perform theoretical yield analysis on.",
            Button("Return", "index")
            ])
    
    list_of_reactants = list(state.reactants.values())
    limiting_reac = list_of_reactants[0]
    desired_prod = state.products[state.desired_product]
    
    for reactant in list_of_reactants:
        yield_LR = ((limiting_reac.mass_g / limiting_reac.molar_mass)
        * (desired_prod.coeff/limiting_reac.coeff)
        * desired_prod.molar_mass
                    )
        
        theoretical_yield = yield_LR
        
        yield_current_reac = ((reactant.mass_g / reactant.molar_mass)
        * (desired_prod.coeff/reactant.coeff)
        * desired_prod.molar_mass)
        
        if yield_current_reac < yield_LR:
            limiting_reac = reactant
            theoretical_yield = yield_current_reac
        state.limiting_reactant = limiting_reac.formula
        state.theoretical_yield = yield_current_reac
        
    return Page(state, [
            "The limiting reactant is:",
            state.limiting_reactant, '\n',
            "Theoretical yield:",
            round(state.theoretical_yield, 3), 'g\n',
            "Percent_yield:",
            round((state.products[state.desired_product].mass_g/state.theoretical_yield)*100, 2),
            "%\n",
            Button("Next", "enthalpy_page"),
            Button("Back", "product_page")
            ])
@route
def enthalpy_page(state: State) -> Page:
    """
    Creates a page that shows the enthalpy value for the reaction and the type of
    reaction.
    
    Args:
        state: current state of the program
    Returns:
        Page: shows the enthalpy values and the type of reaction as well as a button
        to return to index.
    """
    total_H_reac = 0.0
    for reactant in state.reactants.values():
        total_H_reac += (reactant.coeff*reactant.enthalpy)
    total_H_prod = 0.0
    for product in state.products.values():
        total_H_prod += (product.coeff*product.enthalpy)
    state.enthalpy_rxn = total_H_prod - total_H_reac
    
    if state.enthalpy_rxn < 0:
        reaction_type = "Exothermic"
    else:
        reaction_type = "Endothermic"
    return Page(state, [
        "The heat of reaction is:",
        round(state.enthalpy_rxn,2), "kJ/mol",
        "\nThe reaction type is:", reaction_type,
        
        Button("Return", "index")
        ])

assert_equal(enthalpy_page(State(reactants={'HCl': Compound(formula='HCl', mass_g=3.0, molar_mass=36.458000000000006, coeff=1, enthalpy=-92.3), 'NaOH': Compound(formula='NaOH', mass_g=3.0, molar_mass=39.99676928, coeff=1, enthalpy=-416.88)}, products={'H2O': Compound(formula='H2O', mass_g=0.0, molar_mass=18.015, coeff=1, enthalpy=-293.0), 'NaCl': Compound(formula='NaCl', mass_g=4.0, molar_mass=58.43976928000001, coeff=1, enthalpy=-385.92)}, desired_product='NaCl', limiting_reactant='NaOH', theoretical_yield=4.3833367293409555, enthalpy_rxn=0.0, current_reactant=2, current_product=2)),
    Page(State(reactants={'HCl': Compound(formula='HCl',
                                     mass_g=3.0,
                                     molar_mass=36.458000000000006,
                                     coeff=1,
                                     enthalpy=-92.3),
                     'NaOH': Compound(formula='NaOH',
                                      mass_g=3.0,
                                      molar_mass=39.99676928,
                                      coeff=1,
                                      enthalpy=-416.88)},
          products={'H2O': Compound(formula='H2O',
                                    mass_g=0.0,
                                    molar_mass=18.015,
                                    coeff=1,
                                    enthalpy=-293.0),
                    'NaCl': Compound(formula='NaCl',
                                     mass_g=4.0,
                                     molar_mass=58.43976928000001,
                                     coeff=1,
                                     enthalpy=-385.92)},
          desired_product='NaCl',
          limiting_reactant='NaOH',
          theoretical_yield=4.3833367293409555,
          enthalpy_rxn=-169.74000000000007,
          current_reactant=2,
          current_product=2), [
        'The heat of reaction is:',
        -169.74,
        'kJ/mol',
        '\nThe reaction type is:',
        'Exothermic',
        Button('Return', 'index'),
    ]))

start_server(initial_state)
