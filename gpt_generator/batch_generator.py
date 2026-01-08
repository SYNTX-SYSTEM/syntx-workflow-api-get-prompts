"""
Batch Prompt Generator
Generiert mehrere Prompts auf einmal mit verschiedenen Topics und Styles
"""
import json
import random
from datetime import datetime
from .syntx_prompt_generator import generate_prompt  # 🔥 FIX: relative import
from .topics_database import get_random_topics  # 🔥 FIX: relative import
from .prompt_styles import get_all_styles  # 🔥 FIX: relative import
from .cost_tracker import get_total_costs  # 🔥 FIX: relative import

def generate_batch(count: int = 20, use_random_styles: bool = True) -> dict:
    """
    Generiert mehrere Prompts auf einmal.
    
    Args:
        count: Anzahl zu generierender Prompts
        use_random_styles: Ob zufällige Styles verwendet werden sollen
        
    Returns:
        dict mit Ergebnissen und Statistiken
    """
    
    print(f"\n{'='*80}")
    print(f"BATCH GENERATION - {count} Prompts")
    print(f"{'='*80}\n")
    
    # Zufällige Topics holen
    topics = get_random_topics(count)
    styles = get_all_styles()
    
    results = []
    stats = {
        "total": count,
        "successful": 0,
        "refused": 0,
        "errors": 0,
        "by_category": {},
        "by_style": {},
        "total_cost": 0.0,
        "avg_quality": 0.0
    }
    
    for i, (category, topic) in enumerate(topics, 1):
        # Zufälligen Style wählen
        style = random.choice(styles) if use_random_styles else "technisch"
        
        print(f"[{i}/{count}] {category.upper()}: {topic}")
        print(f"   Style: {style}")
        
        # Prompt generieren
        result = generate_prompt(
            prompt=topic,
            style=style,
            category=category,
            max_tokens=500
        )
        
        results.append(result)
        
        # Statistiken updaten
        if result['success']:
            stats["successful"] += 1
            
            # Quality tracking
            if result.get('quality_score'):
                quality = result['quality_score'].get('total_score', 0)
                stats["avg_quality"] += quality
            
            # Cost tracking
            if result.get('cost'):
                stats["total_cost"] += result.get('cost', {}).get('total_cost', 0.0)
            
            print(f"   ✅ Success (Quality: {quality}/100)")
        else:
            if 'refusal' in result.get('error', '').lower():
                stats["refused"] += 1
                print(f"   ⚠️  Refused")
            else:
                stats["errors"] += 1
                print(f"   ❌ Error: {result.get('error', 'Unknown')}")
        
        # Category stats
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        
        # Style stats
        stats["by_style"][style] = stats["by_style"].get(style, 0) + 1
    
    # Durchschnittliche Quality berechnen
    if stats["successful"] > 0:
        stats["avg_quality"] = stats["avg_quality"] / stats["successful"]
    
    # Finale Statistiken ausgeben
    print(f"\n{'='*80}")
    print("BATCH RESULTS")
    print(f"{'='*80}")
    print(f"Total:      {stats['total']}")
    print(f"Successful: {stats['successful']}")
    print(f"Refused:    {stats['refused']}")
    print(f"Errors:     {stats['errors']}")
    print(f"Avg Quality: {stats['avg_quality']:.1f}/100")
    print(f"Total Cost: ${stats['total_cost']:.4f}")
    print(f"\nBy Category:")
    for cat, count in stats["by_category"].items():
        print(f"  {cat}: {count}")
    print(f"\nBy Style:")
    for style, count in stats["by_style"].items():
        print(f"  {style}: {count}")
    print(f"{'='*80}\n")
    
    return {
        "results": results,
        "stats": stats
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch Prompt Generator")
    parser.add_argument("--count", type=int, default=20, help="Anzahl zu generierender Prompts")
    parser.add_argument("--fixed-style", type=str, help="Fixer Style statt zufällig")
    
    args = parser.parse_args()
    
    use_random = args.fixed_style is None
    
    result = generate_batch(
        count=args.count,
        use_random_styles=use_random
    )
