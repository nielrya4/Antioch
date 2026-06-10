from antioch import *
from examples import canvas_macros_demo, chartjs_demo, cloud_sync_demo, custom_macro_example, dataviz_app, dom_demo, example, filesystem_demo, macro_showcase, macros_demo, \
    map_demo, pong_game, quick_macro_test, robust_datatable_demo, style_demo, toolbar_demo, webcanvas_demo, windows_demo, map_layers_demo
from scripts.examples import geospatial_demo, code_block_demo, js_library_wrapper_demo, unified_events_demo, event_patterns, when_decorator_demo, events_namespace_demo, element_events_demo, event_combination_demo, macro_events_demo, parent_children_demo
from tutorials import t01_hello_world, t02_chaining_elements, t03_events
from webpage import main as web_main

def main():
    # The following are demos and tutorials for using Antioch
    # map_layers_demo.main()
    # geospatial_demo.main()
    # example.main()
    # style_demo.main()
    # dom_demo.main()
    # macros_demo.main()
    # toolbar_demo.main()
    # custom_macro_example.main()
    # dataviz_app.main()
    # map_demo.main()
    #windows_demo.main()
    # webcanvas_demo.main()
    # canvas_macros_demo.main()
    # pong_game.main()
    # filesystem_demo.main()
    # cloud_sync_demo.main()
    # robust_datatable_demo.main()
    # macro_showcase.main()
    # quick_macro_test.main()
    # chartjs_demo.main()
    # t01_hello_world.main()
    # t02_chaining_elements.main()
    # t03_events.main()
    # web_main.main()
    # js_library_wrapper_demo.main()
    """from scripts.examples import user_input_modal

    user_input_modal.main()"""

    # code_block_demo.main()
    # from scripts.examples import download_link_demo

    # ========== Event System Demos ==========
    # Old demos (still work but use old patterns):
    # unified_events_demo.main()
    # event_patterns.main()
    # when_decorator_demo.main()

    # New demos (demonstrate .events namespace):
    # events_namespace_demo.main()  # Complete demo of .events namespace
    # element_events_demo.main()    # Element and DOM events with auto-wiring
    # event_combination_demo.main()  # Pre-registered events and | operator

    # Comprehensive macro events demo (showcases all refactored macros):
    # macro_events_demo.main()  # 🎉 All macros with unified event system!

    # Element parent/children demo (tree traversal):
    parent_children_demo.main()  # Element.parent and Element.children

if __name__ == "__main__":
    main()