# test_app.py
# Simple test script to verify the application components

import os
import sys

def test_imports():
    """Test if all modules can be imported successfully"""
    try:
        print("Testing imports...")
        
        # Test translation engine
        from translation_engine import (
            translate_presentation, LANG_OPTIONS, TONE_OPTIONS,
            create_openai_client, create_deepseek_client
        )
        print("OK - translation_engine imported successfully")
        
        # Test accuracy checker
        from accuracy_checker import (
            evaluate_translation_quality, batch_evaluate_translations,
            get_flagged_translations, get_low_confidence_translations
        )
        print("OK - accuracy_checker imported successfully")
        
        # Test comparison UI
        from comparison_ui import (
            create_slide_comparison_ui, create_flagged_translations_ui,
            create_retranslation_ui, extract_slide_text_data
        )
        print("OK - comparison_ui imported successfully")
        
        # Test streamlit app
        import streamlit as st
        print("OK - streamlit imported successfully")
        
        print("\nAll imports successful! The application should work correctly.")
        return True
        
    except ImportError as e:
        print(f"ERROR - Import error: {e}")
        return False
    except Exception as e:
        print(f"ERROR - Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without API calls"""
    try:
        print("\nTesting basic functionality...")
        
        from translation_engine import LANG_OPTIONS, TONE_OPTIONS, is_effectively_empty_tagged
        
        # Test language options
        assert len(LANG_OPTIONS) > 0, "Language options should not be empty"
        print(f"OK - Found {len(LANG_OPTIONS)} language options")
        
        # Test tone options
        assert len(TONE_OPTIONS) > 0, "Tone options should not be empty"
        print(f"OK - Found {len(TONE_OPTIONS)} tone options")
        
        # Test utility functions
        assert is_effectively_empty_tagged("") == True, "Empty string should be empty"
        assert is_effectively_empty_tagged("[[R1]]text[[/R1]]") == False, "Tagged text should not be empty"
        print("OK - Utility functions working correctly")
        
        print("Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"ERROR - Functionality test error: {e}")
        return False

def main():
    """Run all tests"""
    print("Running PPT Translation App Tests\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "="*50)
    if imports_ok and functionality_ok:
        print("All tests passed! The application is ready to use.")
        print("\nTo run the Streamlit app:")
        print("  streamlit run streamlit_app.py")
        print("\nTo run the desktop app:")
        print("  python PPT_Language_Change.py")
    else:
        print("Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
