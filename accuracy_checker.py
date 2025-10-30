# accuracy_checker.py
# AI accuracy evaluation module for translation quality assessment

import re
import time
from typing import Dict, List, Tuple, Optional
from translation_engine import safe_request, create_openai_client, create_deepseek_client


def evaluate_translation_quality(original_text: str, translated_text: str, target_lang: str, 
                                openai_api_key: str, deepseek_api_key: str, use_deepseek: bool = False) -> Dict:
    """
    번역 품질을 평가하고 신뢰도 점수와 문제점을 반환
    
    Returns:
        {
            "confidence_score": 0-100,
            "issues": ["issue1", "issue2"],
            "suggestions": ["suggestion1", "suggestion2"],
            "is_flagged": bool
        }
    """
    if not original_text.strip() or not translated_text.strip():
        return {
            "confidence_score": 0,
            "issues": ["Empty text"],
            "suggestions": ["Check if text was properly extracted"],
            "is_flagged": True
        }
    
    # 중국어 번역의 경우 기존 검토 로직 사용
    if "Chinese" in target_lang:
        return evaluate_chinese_translation(original_text, translated_text, openai_api_key, deepseek_api_key, use_deepseek)
    
    # 다른 언어들의 경우 일반적인 품질 평가
    return evaluate_general_translation(original_text, translated_text, target_lang, openai_api_key)


def evaluate_chinese_translation(original_text: str, translated_text: str, 
                                openai_api_key: str, deepseek_api_key: str, use_deepseek: bool = False) -> Dict:
    """
    중국어 번역의 자연스러움을 검토하고 필요시 수정된 번역을 반환
    """
    if not original_text.strip() or not translated_text.strip():
        return {"confidence_score": 0, "issues": ["Empty text"], "suggestions": [], "is_flagged": True}
    
    review_prompt = (
        f"당신은 중국어 번역 품질을 검토하는 전문가입니다.\n\n"
        f"원문 (한국어): {original_text}\n"
        f"번역문 (중국어): {translated_text}\n\n"
        f"다음을 검토해주세요:\n"
        f"1. 중국 원어민이 읽었을 때 어색하거나 부자연스러운 부분이 있는가?\n"
        f"2. 문법적으로 올바른가?\n"
        f"3. 표현이 자연스러운가?\n"
        f"4. 신뢰도 점수 (0-100점)를 매겨주세요.\n\n"
        f"응답 형식:\n"
        f"신뢰도: [0-100]\n"
        f"어색함: [YES/NO]\n"
        f"문제점: [구체적인 문제점들]\n"
        f"개선제안: [개선 방안들]\n"
        f"수정된 번역: [수정된 중국어 번역 또는 원래 번역]\n\n"
        f"중요: [[R1]]...[[/R1]] 같은 마커 태그는 절대 변경하지 마세요."
    )
    
    try:
        if use_deepseek:
            client = create_deepseek_client(deepseek_api_key)
            content = safe_request(client, review_prompt, retries=2, delay=2, use_deepseek=True)
        else:
            client = create_openai_client(openai_api_key)
            content = safe_request(client, review_prompt, retries=2, delay=2)
            
        if not content:
            return {"confidence_score": 50, "issues": ["Review failed"], "suggestions": [], "is_flagged": True}
        
        # Parse response
        lines = content.strip().split('\n')
        confidence_score = 50  # default
        is_awkward = False
        issues = []
        suggestions = []
        revised_translation = translated_text
        
        for line in lines:
            if line.startswith("신뢰도:"):
                try:
                    score_text = line.replace("신뢰도:", "").strip()
                    confidence_score = int(re.findall(r'\d+', score_text)[0])
                except:
                    confidence_score = 50
            elif line.startswith("어색함:"):
                is_awkward = "YES" in line.upper()
            elif line.startswith("문제점:"):
                issues_text = line.replace("문제점:", "").strip()
                if issues_text:
                    issues = [issue.strip() for issue in issues_text.split(',')]
            elif line.startswith("개선제안:"):
                suggestions_text = line.replace("개선제안:", "").strip()
                if suggestions_text:
                    suggestions = [suggestion.strip() for suggestion in suggestions_text.split(',')]
            elif line.startswith("수정된 번역:"):
                revised_translation = line.replace("수정된 번역:", "").strip()
        
        is_flagged = confidence_score < 70 or is_awkward or len(issues) > 0
        
        return {
            "confidence_score": confidence_score,
            "issues": issues,
            "suggestions": suggestions,
            "is_flagged": is_flagged,
            "revised_translation": revised_translation
        }
        
    except Exception as e:
        print(f"⚠️ Chinese review error: {e}")
        return {"confidence_score": 50, "issues": ["Review error"], "suggestions": [], "is_flagged": True}


def evaluate_general_translation(original_text: str, translated_text: str, target_lang: str, openai_api_key: str) -> Dict:
    """
    일반적인 번역 품질 평가 (중국어 제외)
    """
    evaluation_prompt = (
        f"You are a professional translation quality evaluator. Please evaluate the following translation:\n\n"
        f"Original (Korean): {original_text}\n"
        f"Translation ({target_lang}): {translated_text}\n\n"
        f"Please assess:\n"
        f"1. Translation accuracy and faithfulness to the original\n"
        f"2. Naturalness and fluency in the target language\n"
        f"3. Consistency with beauty industry terminology\n"
        f"4. Overall quality score (0-100)\n\n"
        f"Response format:\n"
        f"Confidence: [0-100]\n"
        f"Accuracy: [EXCELLENT/GOOD/FAIR/POOR]\n"
        f"Naturalness: [EXCELLENT/GOOD/FAIR/POOR]\n"
        f"Issues: [List specific problems, if any]\n"
        f"Suggestions: [List improvement suggestions, if any]\n\n"
        f"Important: Do NOT alter any marker tags like [[R1]]...[[/R1]]."
    )
    
    try:
        client = create_openai_client(openai_api_key)
        content = safe_request(client, evaluation_prompt, retries=2, delay=2)
        
        if not content:
            return {"confidence_score": 50, "issues": ["Evaluation failed"], "suggestions": [], "is_flagged": True}
        
        # Parse response
        lines = content.strip().split('\n')
        confidence_score = 50  # default
        accuracy = "FAIR"
        naturalness = "FAIR"
        issues = []
        suggestions = []
        
        for line in lines:
            if line.startswith("Confidence:"):
                try:
                    score_text = line.replace("Confidence:", "").strip()
                    confidence_score = int(re.findall(r'\d+', score_text)[0])
                except:
                    confidence_score = 50
            elif line.startswith("Accuracy:"):
                accuracy = line.replace("Accuracy:", "").strip()
            elif line.startswith("Naturalness:"):
                naturalness = line.replace("Naturalness:", "").strip()
            elif line.startswith("Issues:"):
                issues_text = line.replace("Issues:", "").strip()
                if issues_text and issues_text != "None":
                    issues = [issue.strip() for issue in issues_text.split(',')]
            elif line.startswith("Suggestions:"):
                suggestions_text = line.replace("Suggestions:", "").strip()
                if suggestions_text and suggestions_text != "None":
                    suggestions = [suggestion.strip() for suggestion in suggestions_text.split(',')]
        
        # Determine if flagged based on score and quality
        is_flagged = (confidence_score < 70 or 
                     accuracy in ["POOR"] or 
                     naturalness in ["POOR"] or 
                     len(issues) > 0)
        
        return {
            "confidence_score": confidence_score,
            "issues": issues,
            "suggestions": suggestions,
            "is_flagged": is_flagged,
            "accuracy": accuracy,
            "naturalness": naturalness
        }
        
    except Exception as e:
        print(f"⚠️ General evaluation error: {e}")
        return {"confidence_score": 50, "issues": ["Evaluation error"], "suggestions": [], "is_flagged": True}


def flag_translation(translation_id: str, reason: str, user_notes: str = "") -> Dict:
    """
    사용자가 수동으로 번역을 플래그하는 함수
    """
    return {
        "translation_id": translation_id,
        "flagged": True,
        "reason": reason,
        "user_notes": user_notes,
        "timestamp": time.time()
    }


def suggest_improvements(original_text: str, translated_text: str, target_lang: str, 
                        openai_api_key: str, specific_issue: str = "") -> List[str]:
    """
    AI가 번역 개선안을 제안하는 함수
    """
    improvement_prompt = (
        f"You are a professional translation consultant. Please suggest improvements for this translation:\n\n"
        f"Original (Korean): {original_text}\n"
        f"Current Translation ({target_lang}): {translated_text}\n"
        f"Target Language: {target_lang}\n"
        f"Specific Issue: {specific_issue if specific_issue else 'General improvement needed'}\n\n"
        f"Please provide 3-5 specific, actionable improvement suggestions.\n"
        f"Focus on:\n"
        f"- Better terminology for beauty industry\n"
        f"- More natural phrasing\n"
        f"- Improved clarity and flow\n"
        f"- Cultural appropriateness\n\n"
        f"Format as a numbered list:\n"
        f"1. [Suggestion 1]\n"
        f"2. [Suggestion 2]\n"
        f"etc.\n\n"
        f"Important: Do NOT alter any marker tags like [[R1]]...[[/R1]]."
    )
    
    try:
        client = create_openai_client(openai_api_key)
        content = safe_request(client, improvement_prompt, retries=2, delay=2)
        
        if not content:
            return ["Unable to generate suggestions at this time."]
        
        # Parse numbered list
        suggestions = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if re.match(r'^\d+\.', line):
                suggestion = re.sub(r'^\d+\.\s*', '', line)
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions if suggestions else ["No specific suggestions available."]
        
    except Exception as e:
        print(f"⚠️ Improvement suggestion error: {e}")
        return ["Unable to generate suggestions due to an error."]


def batch_evaluate_translations(translations_data: List[Dict], target_lang: str, 
                               openai_api_key: str, deepseek_api_key: str, 
                               use_deepseek: bool = False) -> List[Dict]:
    """
    여러 번역을 일괄 평가하는 함수
    """
    results = []
    
    for i, translation_data in enumerate(translations_data):
        print(f"Evaluating translation {i+1}/{len(translations_data)}")
        
        evaluation = evaluate_translation_quality(
            translation_data["original_text"],
            translation_data["translated_text"],
            target_lang,
            openai_api_key,
            deepseek_api_key,
            use_deepseek
        )
        
        # Add metadata
        evaluation["translation_id"] = translation_data.get("id", f"translation_{i}")
        evaluation["slide_number"] = translation_data.get("slide_number", 0)
        evaluation["shape_type"] = translation_data.get("shape_type", "text_frame")
        
        results.append(evaluation)
    
    return results


def get_flagged_translations(evaluation_results: List[Dict]) -> List[Dict]:
    """
    플래그된 번역들만 필터링하여 반환
    """
    return [result for result in evaluation_results if result.get("is_flagged", False)]


def get_low_confidence_translations(evaluation_results: List[Dict], threshold: int = 70) -> List[Dict]:
    """
    낮은 신뢰도 점수의 번역들을 반환
    """
    return [result for result in evaluation_results if result.get("confidence_score", 0) < threshold]
